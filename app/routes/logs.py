# app/routes/logs.py

from fastapi import APIRouter
from app.core.database import get_database
from datetime import datetime

router = APIRouter()
db = get_database()

@router.get("/list")
async def list_logs():
    """
    Retorna os logs recentes do sistema.
    """
    logs = await db["logs"].find().sort("timestamp", -1).limit(50).to_list(None)
    return {"response": "Últimos logs coletados!", "logs": logs}

@router.post("/register")
async def register_log(event: str, level: str = "INFO"):
    """
    Registra um novo log no sistema.
    """
    log_data = {"event": event, "level": level, "timestamp": datetime.utcnow()}
    await db["logs"].insert_one(log_data)
    return {"response": "Log registrado com sucesso!"}
