# Caminho: app/api/v1/deploy.py

from fastapi import APIRouter, HTTPException, Depends
from app.services.deploy_manager import (
    start_deploy, cancel_deploy, rollback_deploy, get_deploy_status, log_deploy_action
)
from app.core.database import get_database
from datetime import datetime
from bson import ObjectId

router = APIRouter()
db = get_database()

@router.get("/status")
async def get_current_deploy_status():
    """
    Retorna o status do último deploy realizado.
    """
    last_deploy = await db["deploys"].find_one(sort=[("timestamp", -1)])
    if not last_deploy:
        return {"message": "Nenhum deploy foi realizado ainda."}

    return {"deploy_status": last_deploy}

@router.post("/start")
async def start_new_deploy():
    """
    Inicia um novo processo de deploy, registra logs e ativa rollback automático em falha.
    """
    try:
        deploy_result = await start_deploy()
        
        # Registrar log do deploy
        await log_deploy_action("Deploy iniciado", deploy_result)

        return {"message": "Deploy iniciado com sucesso!", "details": deploy_result}
    
    except Exception as e:
        # Registrar falha no log e acionar rollback automático
        await log_deploy_action("Falha no deploy, ativando rollback automático", str(e))
        rollback_result = await rollback_deploy("último")

        return {
            "error": "O deploy falhou e foi revertido automaticamente.",
            "rollback_details": rollback_result,
            "error_details": str(e)
        }

@router.post("/cancel/{deploy_id}")
async def cancel_deploy_process(deploy_id: str):
    """
    Cancela um deploy em andamento e registra a ação no log.
    """
    if not ObjectId.is_valid(deploy_id):
        raise HTTPException(status_code=400, detail="ID de deploy inválido.")

    result = await cancel_deploy(deploy_id)

    # Registrar log do cancelamento
    await log_deploy_action(f"Deploy {deploy_id} cancelado", result)

    return {"message": f"Deploy '{deploy_id}' cancelado com sucesso!", "details": result}

@router.post("/rollback/{deploy_id}")
async def rollback_to_previous_version(deploy_id: str):
    """
    Reverte um deploy para a versão anterior e registra a ação.
    """
    if not ObjectId.is_valid(deploy_id):
        raise HTTPException(status_code=400, detail="ID de deploy inválido.")

    result = await rollback_deploy(deploy_id)

    # Registrar log do rollback
    await log_deploy_action(f"Rollback aplicado no deploy {deploy_id}", result)

    return {"message": f"Deploy '{deploy_id}' revertido com sucesso!", "details": result}

@router.get("/history")
async def get_deploy_history():
    """
    Retorna o histórico de deploys realizados, ordenado por data.
    """
    history = await db["deploys"].find().sort("timestamp", -1).to_list(length=50)
    return {"deploy_history": history}
