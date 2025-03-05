# app/routes/logs.py

from fastapi import APIRouter, HTTPException
from app.core.database import get_database
from datetime import datetime

router = APIRouter()

@router.get("/list")
async def list_logs():
    """
    Retorna os logs recentes do sistema.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    try:
        logs = await db["logs"].find().sort("timestamp", -1).limit(50).to_list(None)
        return {"response": "Últimos logs coletados!", "logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar logs: {str(e)}")

@router.post("/register")
async def register_log(event: str, level: str = "INFO"):
    """
    Registra um novo log no sistema.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    try:
        log_data = {"event": event, "level": level, "timestamp": datetime.utcnow()}
        await db["logs"].insert_one(log_data)
        return {"response": "Log registrado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar log: {str(e)}")
