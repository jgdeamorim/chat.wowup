# app/services/security_tuner.py

from datetime import datetime
from app.core.database import get_database
from app.core.security import hash_password
from fastapi import HTTPException
from typing import Dict, Any

db = get_database()

async def analyze_security_threats() -> Dict[str, Any]:
    """
    Analisa logs do sistema para identificar padrões suspeitos e possíveis ameaças.
    """
    security_report = {
        "timestamp": datetime.utcnow(),
        "detected_issues": []
    }

    # Verificação de tentativas de login falhas excessivas
    brute_force_attempts = await detect_brute_force_attacks()
    if brute_force_attempts:
        security_report["detected_issues"].append(brute_force_attempts)

    # Verificação de acessos suspeitos
    suspicious_access = await detect_suspicious_access()
    if suspicious_access:
        security_report["detected_issues"].append(suspicious_access)

    # Verificação de permissões inválidas
    permission_issues = await detect_permission_misuse()
    if permission_issues:
        security_report["detected_issues"].append(permission_issues)

    # Registrar relatório de segurança no banco de dados
    await db["security_audit"].insert_one(security_report)

    return {"message": "Análise de segurança concluída!", "details": security_report}

async def detect_brute_force_attacks() -> Dict[str, Any]:
    """
    Detecta tentativas excessivas de login falhas que indicam possível ataque de força bruta.
    """
    threshold = 5  # Número máximo de tentativas permitidas por IP antes de bloquear
    recent_attempts = await db["auth_logs"].find({"status": "failed"}).sort("timestamp", -1).limit(50).to_list(length=50)

    ip_counts = {}
    for attempt in recent_attempts:
        ip = attempt.get("ip_address", "desconhecido")
        ip_counts[ip] = ip_counts.get(ip, 0) + 1

    brute_force_detected = {ip: count for ip, count in ip_counts.items() if count > threshold}
    
    if brute_force_detected:
        return {
            "category": "brute_force",
            "description": "Detectado possível ataque de força bruta.",
            "affected_ips": brute_force_detected
        }
    return {}

async def detect_suspicious_access() -> Dict[str, Any]:
    """
    Identifica acessos suspeitos com base em localização geográfica ou horários incomuns.
    """
    suspicious_logs = await db["auth_logs"].find({
        "status": "success",
        "geo_location": {"$exists": True}
    }).sort("timestamp", -1).limit(50).to_list(length=50)

    suspicious_entries = [
        log for log in suspicious_logs if log["geo_location"] not in ["Brasil", "Estados Unidos", "Europa"]
    ]

    if suspicious_entries:
        return {
            "category": "suspicious_access",
            "description": "Detectado acesso suspeito fora das regiões habituais.",
            "entries": suspicious_entries
        }
    return {}

async def detect_permission_misuse() -> Dict[str, Any]:
    """
    Detecta tentativas de acesso indevido a módulos administrativos por usuários sem permissão.
    """
    admin_access_attempts = await db["access_logs"].find({
        "role": {"$ne": "admin"},
        "module_accessed": {"$in": ["admin", "logs", "config"]}
    }).sort("timestamp", -1).limit(50).to_list(length=50)

    if admin_access_attempts:
        return {
            "category": "permission_misuse",
            "description": "Usuários não administradores tentaram acessar módulos restritos.",
            "entries": admin_access_attempts
        }
    return {}

async def block_ip(ip_address: str) -> Dict[str, Any]:
    """
    Bloqueia um IP automaticamente ao detectar atividades maliciosas.
    """
    await db["blocked_ips"].insert_one({"ip_address": ip_address, "timestamp": datetime.utcnow()})
    return {"message": f"IP {ip_address} bloqueado devido a atividades suspeitas."}

async def log_security_event(event: Dict[str, Any]):
    """
    Registra um evento de segurança no banco de dados para rastreamento.
    """
    event["timestamp"] = datetime.utcnow()
    await db["security_events"].insert_one(event)
