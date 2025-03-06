from fastapi import APIRouter, HTTPException, Depends
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.database import get_database
from app.models.user_model import User
from typing import List
from datetime import timedelta
import logging

# Configuração de logs
logger = logging.getLogger("users")
logger.setLevel(logging.INFO)

router = APIRouter()

@router.post("/register")
async def register_user(user: User):
    """
    Registra um novo usuário no sistema.
    """
    db = await get_database()
    
    # 🔹 Verifica se a coleção 'users' já existe no banco
    if "users" not in await db.list_collection_names():
        await db.create_collection("users")
    
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado.")

    hashed_password = get_password_hash(user.password)  
    user_data = user.dict()
    user_data["password"] = hashed_password

    await db["users"].insert_one(user_data)
    logger.info(f"✅ Novo usuário registrado: {user.email}")
    return {"response": "Usuário registrado com sucesso!"}

@router.post("/login")
async def login_user(email: str, password: str):
    """
    Autentica o usuário e retorna um token JWT.
    """
    db = await get_database()
    
    user = await db["users"].find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    access_token = await create_access_token(user_id=user["email"], role="user")
    logger.info(f"🔐 Usuário autenticado: {email}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", summary="Lista todos os usuários cadastrados")
async def list_users():
    """
    Retorna uma lista de usuários cadastrados.
    """
    try:
        db = await get_database()
        
        # 🔹 Verifica se a coleção existe antes de tentar buscar dados
        if "users" not in await db.list_collection_names():
            logger.warning("⚠️ A coleção 'users' não existe. Retornando lista vazia.")
            return {"users": []}  # Retorna lista vazia caso não tenha usuários
        
        users = await db["users"].find({}, {"_id": 0, "password": 0}).to_list(None)
        return {"users": users}
    
    except Exception as e:
        logger.error(f"❌ Erro ao listar usuários: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar usuários: {str(e)}")
