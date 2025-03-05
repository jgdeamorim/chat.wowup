# app/services/logging_service.py

import logging
from datetime import datetime
from app.core.database import get_database

# Configuração do logging para evitar conflitos de threads
logging.basicConfig(
    filename="storage/logs/system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

async def log_event(event: str, level: str = "INFO"):
    """
    Registra eventos no banco de dados e no arquivo de logs do sistema.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    log_data = {
        "event": event,
        "level": level,
        "timestamp": datetime.utcnow()
    }

    try:
        await db["logs"].insert_one(log_data)  # 🔹 Garantindo gravação assíncrona correta
        logging.log(getattr(logging, level, logging.INFO), event)
        return {"response": f"Log registrado: {event} - Nível: {level}"}
    except Exception as e:
        return {"error": f"Falha ao registrar log: {str(e)}"}

async def get_recent_logs(limit: int = 50):
    """
    Retorna os últimos logs do sistema.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    try:
        logs = await db["logs"].find().sort("timestamp", -1).limit(limit).to_list(None)
        return {"logs": logs}
    except Exception as e:
        return {"error": f"Erro ao buscar logs: {str(e)}"}
