# app/core/security.py

import os
import jwt
import logging
import bcrypt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from app.core.database import get_redis

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logs
logger = logging.getLogger("security")
logger.setLevel(logging.INFO)

# Configurações de segurança
JWT_SECRET = os.getenv("JWT_SECRET", "supersecreto")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))  # Tempo de expiração do token (1h)
MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", 5))  # Tentativas antes de bloquear
BLOCK_TIME_MINUTES = int(os.getenv("BLOCK_TIME_MINUTES", 30))  # Tempo de bloqueio em minutos

security = HTTPBearer()

async def create_jwt_token(user_id: str, role: str):
    """
    Gera um token JWT válido para autenticação.
    """
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    payload = {"sub": user_id, "role": role, "exp": expiration}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

async def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Valida um token JWT e retorna suas informações.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")

async def hash_password(password: str):
    """
    Hash da senha usando bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

async def verify_password(password: str, hashed_password: str):
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

async def is_ip_blocked(ip_address: str):
    """
    Verifica se o IP está bloqueado devido a tentativas de login excessivas.
    """
    redis = await get_redis()
    attempts = await redis.get(f"failed_attempts:{ip_address}")

    if attempts and int(attempts) >= MAX_LOGIN_ATTEMPTS:
        return True
    return False

async def register_failed_login(ip_address: str):
    """
    Registra uma tentativa de login falha e bloqueia o IP se ultrapassar o limite.
    """
    redis = await get_redis()
    attempts = await redis.incr(f"failed_attempts:{ip_address}")

    if attempts == 1:
        await redis.expire(f"failed_attempts:{ip_address}", BLOCK_TIME_MINUTES * 60)

    if attempts >= MAX_LOGIN_ATTEMPTS:
        logger.warning(f"🚨 IP {ip_address} bloqueado por excesso de tentativas!")
        raise HTTPException(status_code=403, detail="Muitas tentativas de login. Tente novamente mais tarde.")

async def reset_failed_attempts(ip_address: str):
    """
    Reseta o contador de falhas ao logar com sucesso.
    """
    redis = await get_redis()
    await redis.delete(f"failed_attempts:{ip_address}")

async def logout_user(token: str):
    """
    Invalida o token do usuário no Redis, garantindo logout seguro.
    """
    redis = await get_redis()
    await redis.setex(f"blacklist:{token}", JWT_EXPIRATION_MINUTES * 60, "invalid")
    return {"message": "Usuário deslogado com sucesso."}

async def is_token_blacklisted(token: str):
    """
    Verifica se o token foi revogado (logout realizado).
    """
    redis = await get_redis()
    if await redis.get(f"blacklist:{token}"):
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")
