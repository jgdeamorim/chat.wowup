# app/api/v1/frontend_sync.py

from fastapi import APIRouter, HTTPException, Depends
from app.services.frontend_sync_manager import sync_frontend, detect_frontend_changes, revert_sync, get_sync_status, generate_full_frontend_json
from app.core.database import get_database
from datetime import datetime
from bson import ObjectId

router = APIRouter()
db = get_database()

@router.get("/status")
async def get_frontend_sync_status():
    """
    Retorna o status da última sincronização entre frontend e backend.
    """
    last_sync = await db["frontend_sync"].find_one(sort=[("timestamp", -1)])
    if not last_sync:
        return {"message": "Nenhuma sincronização realizada ainda."}
    
    return {"sync_status": last_sync}

@router.post("/sync")
async def sync_frontend_with_backend():
    """
    Inicia manualmente a sincronização do frontend com os novos endpoints do backend.
    """
    sync_result = await sync_frontend()
    return {"message": "Sincronização do frontend iniciada com sucesso!", "details": sync_result}

@router.get("/changes")
async def get_frontend_changes():
    """
    Lista as mudanças detectadas que precisam ser refletidas no frontend.
    """
    changes = await detect_frontend_changes()
    return {"pending_changes": changes}

@router.get("/history")
async def get_sync_history():
    """
    Retorna o histórico de sincronizações realizadas.
    """
    history = await db["frontend_sync"].find().sort("timestamp", -1).to_list(length=50)
    return {"sync_history": history}

@router.delete("/revert/{sync_id}")
async def revert_frontend_sync(sync_id: str):
    """
    Reverte uma sincronização do frontend para a versão anterior.
    """
    if not ObjectId.is_valid(sync_id):
        raise HTTPException(status_code=400, detail="ID de sincronização inválido.")

    result = await revert_sync(sync_id)
    return {"message": f"Sincronização '{sync_id}' revertida com sucesso!", "details": result}

@router.get("/full-json")
async def get_full_frontend_json():
    """
    Retorna um JSON completo com menus, páginas e endpoints disponíveis para o frontend.
    """
    full_json = await generate_full_frontend_json()
    return {"frontend_structure": full_json}
