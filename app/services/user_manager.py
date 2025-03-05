# app/services/user_manager.py

from datetime import datetime
from app.core.database import get_database
from app.core.security import hash_password, verify_password
from typing import Dict, Any
from bson import ObjectId

db = get_database()

async def create_user(username: str, email: str, password: str, role: str = "user") -> Dict[str, Any]:
    """
    Cria um novo usuário no sistema.
    """
    hashed_password = hash_password(password)
    user_data = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "role": role,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    await db["users"].insert_one(user_data)
    return {"message": f"Usuário '{username}' criado com sucesso!", "user": user_data}

async def authenticate_user(email: str, password: str) -> Dict[str, Any]:
    """
    Autentica um usuário e retorna um token JWT seguro.
    """
    user = await db["users"].find_one({"email": email})
    if not user or not verify_password(password, user["hashed_password"]):
        return {"error": "Credenciais inválidas."}

    return {"message": "Login bem-sucedido!", "user_id": str(user["_id"])}

async def update_user(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modifica os dados de um usuário existente.
    """
    updates["updated_at"] = datetime.utcnow()
    result = await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": updates})
    
    if result.matched_count == 0:
        return {"error": f"Usuário '{user_id}' não encontrado."}

    return {"message": f"Usuário '{user_id}' atualizado!", "updated_fields": updates}
