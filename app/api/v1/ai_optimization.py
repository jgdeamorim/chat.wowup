# app/api/v1/ai_optimization.py

from fastapi import APIRouter, HTTPException, Depends
from app.services.ai_optimizer import analyze_system, apply_optimization, revert_optimization
from app.core.database import get_database
from datetime import datetime
from bson import ObjectId

router = APIRouter()
db = get_database()

@router.get("/status")
async def get_optimization_status():
    """
    Retorna o status atual do motor de otimização da IA.
    """
    try:
        last_analysis = await db["ai_optimizations"].find_one(sort=[("timestamp", -1)])
        pending_count = await db["ai_optimizations"].count_documents({"status": "pending"})

        status = {
            "ai_optimizer_active": True,
            "last_analysis": last_analysis if last_analysis else "Nenhuma análise realizada ainda.",
            "pending_optimizations": pending_count
        }
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar status da IA: {str(e)}")

@router.post("/analyze")
async def analyze_system_optimization():
    """
    A IA analisa todos os módulos e sugere otimizações baseadas em logs e aprendizado contínuo.
    """
    try:
        analysis_result = await analyze_system()
        return {"message": "Análise concluída! Sugestões de otimização foram geradas.", "details": analysis_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao analisar o sistema: {str(e)}")

@router.post("/apply/{module_name}")
async def apply_ai_optimization(module_name: str):
    """
    Aplica uma otimização sugerida para um módulo específico.
    """
    try:
        if not module_name:
            raise HTTPException(status_code=400, detail="O nome do módulo não pode estar vazio.")

        module = await db["modules"].find_one({"name": module_name})
        if not module:
            raise HTTPException(status_code=404, detail=f"Módulo '{module_name}' não encontrado.")

        result = await apply_optimization(module_name)
        return {"message": f"Otimização aplicada ao módulo '{module_name}' com sucesso!", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao aplicar otimização: {str(e)}")

@router.get("/history")
async def get_optimization_history(limit: int = 50):
    """
    Retorna o histórico de otimizações aplicadas pela IA, limitando a quantidade retornada.
    """
    try:
        history = await db["ai_optimizations"].find().sort("timestamp", -1).to_list(length=limit)
        if not history:
            return {"message": "Nenhuma otimização foi registrada ainda."}
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar histórico de otimizações: {str(e)}")

@router.delete("/revert/{optimization_id}")
async def revert_ai_optimization(optimization_id: str):
    """
    Reverte uma otimização aplicada anteriormente.
    """
    try:
        if not ObjectId.is_valid(optimization_id):
            raise HTTPException(status_code=400, detail="ID de otimização inválido.")

        optimization = await db["ai_optimizations"].find_one({"_id": ObjectId(optimization_id)})
        if not optimization:
            raise HTTPException(status_code=404, detail=f"Otimização '{optimization_id}' não encontrada.")

        result = await revert_optimization(optimization_id)
        return {"message": f"Otimização '{optimization_id}' revertida com sucesso!", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao reverter otimização: {str(e)}")
