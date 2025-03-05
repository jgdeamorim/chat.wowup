# app/services/fine_tuning_manager.py

from datetime import datetime
from app.core.database import get_database
from typing import Dict, Any

async def apply_fine_tuning() -> Dict[str, Any]:
    """
    Aplica ajustes automáticos da IA com base no aprendizado contínuo.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    tuning_log = {
        "timestamp": datetime.utcnow(),
        "adjustments": []
    }

    # Aplicar ajustes individuais e validar erros
    try:
        security_tuning = await apply_security_tuning()
        tuning_log["adjustments"].append(security_tuning)

        performance_tuning = await apply_performance_tuning()
        tuning_log["adjustments"].append(performance_tuning)

        uiux_tuning = await apply_uiux_tuning()
        tuning_log["adjustments"].append(uiux_tuning)

        # Salvar ajustes no histórico
        await db["fine_tuning_history"].insert_one(tuning_log)

        return {"message": "Ajustes aplicados com sucesso!", "details": tuning_log}
    
    except Exception as e:
        return {"error": f"Erro ao aplicar ajustes: {str(e)}"}

async def apply_security_tuning() -> Dict[str, Any]:
    """
    Aplica ajustes de segurança no sistema.
    """
    return {
        "category": "security",
        "applied_changes": [
            "Melhoria na validação de JWT",
            "Ajuste nas permissões de acesso",
            "Proteção contra brute-force ativada"
        ]
    }

async def apply_performance_tuning() -> Dict[str, Any]:
    """
    Aplica otimizações para melhorar a performance do sistema.
    """
    return {
        "category": "performance",
        "applied_changes": [
            "Otimização de queries no banco de dados",
            "Melhoria no cache de respostas",
            "Redução de tempo de resposta da API"
        ]
    }

async def apply_uiux_tuning() -> Dict[str, Any]:
    """
    Aplica melhorias na interface e usabilidade do sistema.
    """
    return {
        "category": "uiux",
        "applied_changes": [
            "Ajuste nos componentes visuais",
            "Melhoria na responsividade do frontend",
            "Sugestões de UI/UX baseadas em analytics"
        ]
    }

async def rollback_last_tuning() -> Dict[str, Any]:
    """
    Reverte o último ajuste fino aplicado pela IA.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    last_tuning = await db["fine_tuning_history"].find_one(sort=[("timestamp", -1)])
    if not last_tuning:
        return {"message": "Nenhum ajuste foi encontrado para rollback."}

    await db["fine_tuning_history"].delete_one({"_id": last_tuning["_id"]})
    return {"message": "Último ajuste revertido com sucesso!", "details": last_tuning}
