# app/api/v1/admin.py

from fastapi import APIRouter, HTTPException, Depends
from app.services.admin_manager import (
    update_system_config, get_system_logs, clear_logs, set_user_permission, remove_user, get_users_list
)
from app.core.database import get_database
from datetime import datetime
from bson import ObjectId

router = APIRouter()
db = get_database()

@router.get("/system-status")
async def get_system_status():
    """
    Retorna o status geral do sistema e dos serviços ativos.
    """
    try:
        db_status = "Online" if await db.client.server_info() else "Offline"
    except Exception:
        db_status = "Offline"

    status = {
        "database": db_status,
        "ai_optimizer": "Ativo",
        "logs_service": "Ativo",
        "api_version": "1.20"
    }
    return {"system_status": status}

@router.get("/configurations")
async def get_system_configurations():
    """
    Obtém as configurações atuais do sistema.
    """
    config = await db["system_config"].find_one({}, {"_id": 0})
    if not config:
        raise HTTPException(status_code=404, detail="Nenhuma configuração encontrada.")

    return {"configurations": config}

@router.put("/update-configurations")
async def update_configurations(request: dict):
    """
    Modifica as configurações gerais do sistema.
    """
    if not request:
        raise HTTPException(status_code=400, detail="Nenhuma configuração fornecida.")

    result = await update_system_config(request)
    return {"message": "Configurações do sistema atualizadas com sucesso!", "details": result}

@router.get("/logs")
async def get_admin_logs(limit: int = 50):
    """
    Retorna os logs administrativos e de sistema, limitando a quantidade retornada.
    """
    logs = await get_system_logs(limit)
    return {"logs": logs}

@router.delete("/clear-logs")
async def clear_system_logs():
    """
    Limpa os logs do sistema administrativo.
    """
    result = await clear_logs()
    return {"message": "Logs do sistema foram limpos com sucesso!", "details": result}

@router.post("/set-permission/{user_id}")
async def set_permission(user_id: str, request: dict):
    """
    Define permissões para um usuário específico.
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID de usuário inválido.")

    new_role = request.get("role", "").strip().lower()  # admin | user | viewer
    if new_role not in ["admin", "user", "viewer"]:
        raise HTTPException(status_code=400, detail="Nível de permissão inválido.")

    result = await set_user_permission(user_id, new_role)
    return {"message": f"Permissão do usuário '{user_id}' alterada para '{new_role}'.", "details": result}

@router.get("/users")
async def list_users(limit: int = 50):
    """
    Lista todos os usuários cadastrados no sistema com um limite máximo de retorno.
    """
    users = await get_users_list(limit)
    return {"users": users}

@router.delete("/remove-user/{user_id}")
async def remove_user_from_system(user_id: str):
    """
    Remove um usuário do sistema de forma segura.
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID de usuário inválido.")

    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuário '{user_id}' não encontrado.")

    result = await remove_user(user_id)
    return {"message": f"Usuário '{user_id}' removido com sucesso!", "details": result}
