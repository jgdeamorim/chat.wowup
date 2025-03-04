# app/routes/system.py

from fastapi import APIRouter
import os
import subprocess

router = APIRouter()

@router.get("/status")
async def get_system_status():
    """
    Retorna o status atual do sistema.
    """
    return {"status": "Online", "version": "1.20"}

@router.post("/deploy")
async def deploy_system():
    """
    Executa o processo de deploy automatizado.
    """
    try:
        subprocess.run(["docker-compose", "up", "-d", "--build"], check=True)
        return {"response": "Deploy realizado com sucesso!"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/logs")
async def get_system_logs():
    """
    Retorna os logs do sistema.
    """
    logs = subprocess.check_output(["docker", "logs", "--tail", "100", "chat-central"])
    return {"logs": logs.decode("utf-8")}
