# app/services/admin_manager.py

from datetime import datetime
from app.core.database import get_database
from bson import ObjectId
from typing import Dict, Any

async def update_system_config(db, config_updates: Dict[str, Any]):
    """
    Atualiza as configurações gerais do sistema.
    """
    await db["system_config"].update_one({}, {"$set": config_updates}, upsert=True)
    return {"message": "Configurações do sistema atualizadas.", "updates": config_updates}

async def get_system_logs(db, limit: int = 50):
    """
    Retorna os logs administrativos e de sistema.
    """
    logs = await db["logs"].find().sort("timestamp", -1).limit(limit).to_list(None)
    return logs

async def clear_logs(db):
    """
    Remove todos os logs administrativos do sistema.
    """
    result = await db["logs"].delete_many({})
    return {"message": f"{result.deleted_count} logs removidos com sucesso!"}

async def set_user_permission(db, user_id: str, role: str):
    """
    Define a permissão de um usuário no sistema.
    """
    if role not in ["admin", "user", "viewer"]:
        return {"error": "Nível de permissão inválido. Escolha entre: admin, user, viewer."}

    result = await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": {"role": role}})
    if result.matched_count == 0:
        return {"error": f"Usuário '{user_id}' não encontrado."}

    return {"message": f"Permissão do usuário '{user_id}' alterada para '{role}'."}

async def remove_user(db, user_id: str):
    """
    Remove um usuário do sistema.
    """
    result = await db["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        return {"error": f"Usuário '{user_id}' não encontrado."}

    return {"message": f"Usuário '{user_id}' removido com sucesso!"}

async def get_users_list(db, limit: int = 50):
    """
    Retorna a lista de usuários cadastrados no sistema.
    """
    users = await db["users"].find().sort("created_at", -1).limit(limit).to_list(None)
    return users
