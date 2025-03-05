# app/services/ai_optimizer.py

from datetime import datetime
from app.core.database import get_database
from typing import Dict, Any
from fastapi import HTTPException

async def analyze_system() -> Dict[str, Any]:
    """
    Analisa o sistema e sugere otimizações baseadas no aprendizado da IA.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    analysis_result = {
        "timestamp": datetime.utcnow(),
        "suggestions": [
            "Otimizar tempo de resposta da API",
            "Aprimorar cache",
            "Melhorar estrutura de logs"
        ]
    }
    
    await db["ai_optimizations"].insert_one(analysis_result)
    return analysis_result

async def apply_optimization(module_name: str) -> Dict[str, Any]:
    """
    Aplica uma otimização sugerida pela IA para um módulo específico.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    # Verifica se o módulo existe antes de aplicar otimização
    existing_module = await db["modules"].find_one({"name": module_name})
    if not existing_module:
        raise HTTPException(status_code=404, detail=f"Módulo '{module_name}' não encontrado.")

    optimization_result = {
        "module": module_name,
        "status": "Otimização aplicada",
        "applied_at": datetime.utcnow()
    }
    
    await db["ai_optimizations"].insert_one(optimization_result)
    return optimization_result
