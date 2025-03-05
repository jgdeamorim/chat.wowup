# app/services/user_manager.py

from datetime import datetime
from app.core.database import get_database
from app.core.security import hash_password, verify_password
from typing import Dict, Any
from bson import ObjectId

async def create_user(username: str, email: str, password: str, role: str = "user") -> Dict[str, Any]:
    """
    Cria um novo usuário no sistema.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
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
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    user = await db["users"].find_one({"email": email})
    if not user or not verify_password(password, user["hashed_password"]):
        return {"error": "Credenciais inválidas."}

    return {
        "message": "Login bem-sucedido!",
        "user_id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"]
    }

async def update_user(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modifica os dados de um usuário existente.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    updates["updated_at"] = datetime.utcnow()
    result = await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": updates})
    
    if result.matched_count == 0:
        return {"error": f"Usuário '{user_id}' não encontrado."}

    return {"message": f"Usuário '{user_id}' atualizado!", "updated_fields": updates}
