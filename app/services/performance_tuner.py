# app/services/performance_tuner.py

from datetime import datetime
from app.core.database import get_database
from app.core.cache import get_redis_cache
from fastapi import HTTPException
from typing import Dict, Any

db = get_database()
redis_cache = get_redis_cache()

async def analyze_performance() -> Dict[str, Any]:
    """
    Analisa logs do sistema para identificar endpoints com desempenho abaixo do esperado.
    """
    performance_report = {
        "timestamp": datetime.utcnow(),
        "slow_endpoints": [],
        "cache_optimizations": []
    }

    # Identificar endpoints lentos com base no tempo de resposta médio
    slow_endpoints = await detect_slow_endpoints()
    if slow_endpoints:
        performance_report["slow_endpoints"].extend(slow_endpoints)

    # Verificar se algum endpoint pode ser otimizado via cache
    cache_optimizations = await detect_cache_opportunities()
    if cache_optimizations:
        performance_report["cache_optimizations"].extend(cache_optimizations)

    # Registrar relatório de otimização no banco de dados
    await db["performance_audit"].insert_one(performance_report)

    return {"message": "Análise de desempenho concluída!", "details": performance_report}

async def detect_slow_endpoints() -> Dict[str, Any]:
    """
    Detecta endpoints com tempo de resposta superior ao limite recomendado.
    """
    threshold = 500  # Tempo limite em milissegundos
    slow_requests = await db["api_logs"].find({"response_time": {"$gt": threshold}}).sort("response_time", -1).limit(10).to_list(length=10)

    if slow_requests:
        return {
            "category": "slow_endpoints",
            "description": "Endpoints com tempo de resposta acima do limite recomendado.",
            "affected_endpoints": [{"route": req["route"], "response_time": req["response_time"]} for req in slow_requests]
        }
    return {}

async def detect_cache_opportunities() -> Dict[str, Any]:
    """
    Identifica endpoints que podem se beneficiar de cache dinâmico.
    """
    high_frequency_routes = await db["api_logs"].aggregate([
        {"$group": {"_id": "$route", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 50}}},  # Somente endpoints acessados frequentemente
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]).to_list(length=5)

    if high_frequency_routes:
        return {
            "category": "cache_optimizations",
            "description": "Endpoints frequentemente acessados podem ser otimizados com cache.",
            "suggested_cache_routes": [{"route": route["_id"], "access_count": route["count"]} for route in high_frequency_routes]
        }
    return {}

async def apply_cache_optimization(route: str, ttl: int = 300) -> Dict[str, Any]:
    """
    Aplica cache dinâmico em um endpoint específico para otimizar o desempenho.
    """
    if not route:
        raise HTTPException(status_code=400, detail="A rota do endpoint não pode estar vazia.")

    redis_cache.setex(f"cache:{route}", ttl, "ENABLED")
    return {"message": f"Cache ativado para '{route}' por {ttl} segundos."}

async def clear_cache(route: str) -> Dict[str, Any]:
    """
    Remove o cache de um endpoint específico.
    """
    redis_cache.delete(f"cache:{route}")
    return {"message": f"Cache removido para '{route}'."}

async def log_performance_event(event: Dict[str, Any]):
    """
    Registra um evento de otimização de desempenho no banco de dados.
    """
    event["timestamp"] = datetime.utcnow()
    await db["performance_events"].insert_one(event)
