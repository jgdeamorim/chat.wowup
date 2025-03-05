# app/routes/admin.py

from fastapi import APIRouter, HTTPException, Depends
from app.core.security import admin_required
from app.core.database import get_database

router = APIRouter()

@router.get("/dashboard")
async def get_admin_dashboard():
    """
    Retorna estatísticas do sistema para o painel administrativo.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await`
    try:
        user_count = await db["users"].count_documents({})
        module_count = await db["modules"].count_documents({})
        log_count = await db["logs"].count_documents({})

        return {
            "users": user_count,
            "modules": module_count,
            "logs": log_count,
            "status": "Painel Administrativo Online"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados do painel: {str(e)}")

@router.post("/config/update")
async def update_system_config(config_data: dict, user=Depends(admin_required)):
    """
    Atualiza configurações globais do sistema.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await`
    try:
        await db["system_config"].update_one({}, {"$set": config_data}, upsert=True)
        return {"response": "Configurações atualizadas com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar configurações: {str(e)}")

@router.get("/config")
async def get_system_config():
    """
    Retorna as configurações globais do sistema.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await`
    try:
        config = await db["system_config"].find_one() or {}
        return {"response": "Configurações do sistema", "config": config}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter configurações: {str(e)}")
