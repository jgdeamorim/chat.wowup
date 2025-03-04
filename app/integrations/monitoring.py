# app/integrations/monitoring.py

import psutil
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/status")
async def system_status():
    """
    Retorna métricas do sistema como uso de CPU e memória.
    """
    status = {
        "timestamp": datetime.utcnow(),
        "cpu_usage": f"{psutil.cpu_percent()}%",
        "memory_usage": f"{psutil.virtual_memory().percent}%",
        "disk_usage": f"{psutil.disk_usage('/').percent}%"
    }
    
    return {"response": "Monitoramento do sistema concluído!", "status": status}

@router.get("/api-health")
async def api_health():
    """
    Verifica se a API está funcional e responde corretamente.
    """
    return {"status": "API Online", "timestamp": datetime.utcnow()}
