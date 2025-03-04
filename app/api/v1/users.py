# app/api/v1/users.py

from fastapi import APIRouter, HTTPException, Depends
from app.services.user_manager import (
    create_user, update_user, delete_user, set_user_permission, authenticate_user, request_password_reset
)
from app.core.database import get_database
from app.core.security import generate_jwt_token, hash_password, verify_password
from datetime import datetime
from bson import ObjectId

router = APIRouter()
db = get_database()

# Dicionário para rastrear tentativas de login
failed_login_attempts = {}

@router.get("/")
async def list_users():
    """
    Lista todos os usuários cadastrados no sistema.
    """
    users = await db["users"].find().sort("created_at", -1).to_list(length=50)
    return {"users": users}

@router.get("/{user_id}")
async def get_user_details(user_id: str):
    """
    Retorna detalhes sobre um usuário específico.
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID de usuário inválido.")

    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuário '{user_id}' não encontrado.")
    
    return {"user": user}

@router.post("/create")
async def create_new_user(request: dict):
    """
    Cria um novo usuário no sistema com senha segura e permissões definidas.
    """
    username = request.get("username", "").strip()
    email = request.get("email", "").strip()
    password = request.get("password", "").strip()
    role = request.get("role", "user")  # admin | user | viewer

    if not username or not email or not password:
        raise HTTPException(status_code=400, detail="Nome, e-mail e senha são obrigatórios.")

    hashed_password = hash_password(password)

    result = await create_user(username, email, hashed_password, role)
    return {"message": f"Usuário '{username}' criado com sucesso!", "details": result}

@router.put("/update/{user_id}")
async def update_existing_user(user_id: str, request: dict):
    """
    Modifica os dados de um usuário existente.
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID de usuário inválido.")

    updates = request.get("updates", {})
    if not updates:
        raise HTTPException(status_code=400, detail="Nenhuma atualização fornecida.")

    result = await update_user(user_id, updates)
    return {"message": f"Usuário '{user_id}' atualizado!", "details": result}

@router.delete("/delete/{user_id}")
async def delete_existing_user(user_id: str):
    """
    Remove um usuário do sistema.
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID de usuário inválido.")

    result = await delete_user(user_id)
    return {"message": f"Usuário '{user_id}' removido com sucesso!", "details": result}

@router.post("/set-permission/{user_id}")
async def set_user_permission_level(user_id: str, request: dict):
    """
    Define permissões específicas para um usuário.
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID de usuário inválido.")

    new_role = request.get("role", "user")  # admin | user | viewer
    result = await set_user_permission(user_id, new_role)
    return {"message": f"Permissão do usuário '{user_id}' alterada para '{new_role}'.", "details": result}

@router.get("/roles")
async def get_user_roles():
    """
    Retorna os diferentes níveis de acesso disponíveis no sistema.
    """
    roles = {
        "admin": "Acesso total ao sistema",
        "user": "Acesso limitado a funcionalidades do Chat Central",
        "viewer": "Somente leitura de logs e histórico"
    }
    return {"roles": roles}

@router.post("/login")
async def login(request: dict):
    """
    Autentica um usuário e retorna um token JWT seguro.
    Implementa proteção contra brute-force bloqueando usuários após 5 tentativas falhas.
    """
    email = request.get("email", "").strip()
    password = request.get("password", "").strip()

    if not email or not password:
        raise HTTPException(status_code=400, detail="E-mail e senha são obrigatórios.")

    user = await authenticate_user(email, password)
    if not user:
        # Registra a tentativa falha
        failed_login_attempts[email] = failed_login_attempts.get(email, 0) + 1
        
        # Bloqueia após 5 tentativas
        if failed_login_attempts[email] >= 5:
            raise HTTPException(status_code=403, detail="Muitas tentativas falhas. Conta temporariamente bloqueada.")

        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    # Resetar contador de falhas após sucesso
    failed_login_attempts[email] = 0

    token = generate_jwt_token(user)
    return {"message": "Login bem-sucedido!", "token": token}

@router.post("/password-reset")
async def password_reset(request: dict):
    """
    Envia um e-mail para redefinição de senha.
    """
    email = request.get("email", "").strip()
    if not email:
        raise HTTPException(status_code=400, detail="E-mail é obrigatório.")

    result = await request_password_reset(email)
    return {"message": "Se o e-mail estiver cadastrado, um link de redefinição será enviado.", "details": result}
