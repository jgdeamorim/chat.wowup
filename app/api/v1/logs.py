# Caminho: app/api/v1/logs.py

from fastapi import APIRouter, HTTPException, Query
from app.core.database import get_database
from datetime import datetime
from bson import ObjectId
from typing import Optional

router = APIRouter()
db = get_database()

async def trigger_alert(log_entry):
    """
    Dispara um alerta automático se um log de erro crítico for detectado.
    """
    if log_entry.get("log_type") == "error":
        # Aqui pode ser implementado envio de e-mail, webhook ou notificação
        print(f"🚨 ALERTA CRÍTICO: {log_entry}")

@router.get("/")
async def get_logs(
    log_type: Optional[str] = Query(None, description="Filtrar logs por tipo (info, warning, error)"),
    start_date: Optional[str] = Query(None, description="Filtrar logs a partir desta data (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Filtrar logs até esta data (YYYY-MM-DD)"),
    limit: Optional[int] = Query(50, description="Número máximo de logs a serem retornados")
):
    """
    Retorna os logs do sistema, com possibilidade de filtragem por tipo e período.
    """
    query = {}

    try:
        if log_type:
            query["log_type"] = log_type
        if start_date:
            query["timestamp"] = {"$gte": datetime.strptime(start_date, "%Y-%m-%d")}
        if end_date:
            query.setdefault("timestamp", {})["$lte"] = datetime.strptime(end_date, "%Y-%m-%d")
        
        logs = await db["logs"].find(query).sort("timestamp", -1).limit(limit).to_list(length=limit)
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar logs: {str(e)}")

@router.get("/{log_id}")
async def get_log_details(log_id: str):
    """
    Obtém detalhes de um log específico pelo seu ID.
    """
    if not ObjectId.is_valid(log_id):
        raise HTTPException(status_code=400, detail="ID de log inválido.")

    try:
        log = await db["logs"].find_one({"_id": ObjectId(log_id)})
        if not log:
            raise HTTPException(status_code=404, detail=f"Log '{log_id}' não encontrado.")

        return {"log": log}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar log: {str(e)}")

@router.delete("/clear")
async def clear_all_logs():
    """
    Remove todos os logs do sistema.
    """
    try:
        result = await db["logs"].delete_many({})
        return {"message": f"{result.deleted_count} logs removidos com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar logs: {str(e)}")

@router.delete("/delete/{log_id}")
async def delete_specific_log(log_id: str):
    """
    Exclui um log específico do sistema.
    """
    if not ObjectId.is_valid(log_id):
        raise HTTPException(status_code=400, detail="ID de log inválido.")

    try:
        result = await db["logs"].delete_one({"_id": ObjectId(log_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"Log '{log_id}' não encontrado.")

        return {"message": f"Log '{log_id}' removido com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir log: {str(e)}")
