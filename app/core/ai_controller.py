# app/core/ai_controller.py

import logging
import json
import os
from datetime import datetime
from app.core.database import get_database
from app.services.ai_optimizer import analyze_system, apply_optimization, revert_optimization

# Configuração de logs
logger = logging.getLogger("ai_controller")
logger.setLevel(logging.INFO)

# Carregar configurações da IA
AI_CONFIG_PATH = "config/ai_control.json"

async def load_ai_config():
    """
    Carrega as configurações da IA a partir do JSON de controle.
    """
    try:
        with open(AI_CONFIG_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning("Arquivo de configuração da IA não encontrado. Usando configurações padrão.")
        return {"optimization_level": "moderada", "log_decisions": True}

async def log_ai_decision(action: str, details: dict):
    """
    Registra decisões da IA no banco de dados para rastreamento e aprendizado contínuo.
    """
    db = await get_database()
    decision_log = {
        "timestamp": datetime.utcnow(),
        "action": action,
        "details": details
    }
    await db["ai_decisions"].insert_one(decision_log)
    logger.info(f"🔍 Decisão da IA registrada: {action}")

async def analyze_and_optimize():
    """
    Executa a análise e otimização do sistema com base no nível configurado.
    """
    config = await load_ai_config()
    level = config.get("optimization_level", "moderada")

    if level not in ["leve", "moderada", "agressiva", "controle total"]:
        level = "moderada"  # Garantir que um nível válido esteja definido
    
    logger.info(f"🚀 Iniciando otimização da IA no nível: {level}")

    analysis_result = await analyze_system()
    suggested_optimizations = analysis_result.get("suggestions", [])

    applied_optimizations = []
    for optimization in suggested_optimizations:
        if level in ["moderada", "agressiva", "controle total"]:
            result = await apply_optimization(optimization["module"])
            applied_optimizations.append(result)

    await log_ai_decision("analyze_and_optimize", {
        "level": level,
        "applied_optimizations": applied_optimizations
    })
    
    return {"status": "completed", "applied": applied_optimizations}

async def rollback_ai_changes(optimization_id: str):
    """
    Reverte uma otimização aplicada pela IA, caso necessário.
    """
    result = await revert_optimization(optimization_id)
    await log_ai_decision("rollback", {"optimization_id": optimization_id})
    return {"message": f"Otimização '{optimization_id}' revertida.", "details": result}

async def get_ai_decision_history():
    """
    Retorna o histórico de decisões da IA para auditoria e melhorias futuras.
    """
    db = await get_database()
    decisions = await db["ai_decisions"].find().sort("timestamp", -1).to_list(length=50)
    return {"history": decisions}

async def update_ai_config(new_config: dict):
    """
    Atualiza as configurações da IA e salva no arquivo JSON.
    """
    try:
        with open(AI_CONFIG_PATH, "w") as file:
            json.dump(new_config, file, indent=4)
        logger.info("⚙️ Configuração da IA atualizada com sucesso.")
        return {"message": "Configuração da IA atualizada."}
    except Exception as e:
        logger.error(f"Erro ao atualizar configurações da IA: {str(e)}")
        raise
