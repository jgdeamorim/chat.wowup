# app/services/logging_service.py

import logging
from datetime import datetime
from app.core.database import get_database

db = get_database()

# Configuração do logging
logging.basicConfig(
    filename="storage/logs/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

async def log_event(event: str, level: str = "INFO"):
    """
    Registra eventos no banco de dados e no arquivo de logs do sistema.
    """
    log_data = {
        "event": event,
        "level": level,
        "timestamp": datetime.utcnow()
    }

    await db["logs"].insert_one(log_data)
    logging.log(getattr(logging, level), event)

    return {"response": f"Log registrado: {event} - Nível: {level}"}

async def get_recent_logs(limit: int = 50):
    """
    Retorna os últimos logs do sistema.
    """
    logs = await db["logs"].find().sort("timestamp", -1).limit(limit).to_list(None)
    return {"logs": logs}
