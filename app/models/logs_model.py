# app/models/logs_model.py

from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class LogEntry(BaseModel):
    """
    Representa uma entrada de log no sistema.
    """
    timestamp: datetime = datetime.utcnow()
    nivel: str  # Exemplo: 'info', 'warning', 'error'
    origem: str  # Exemplo: 'auth', 'admin', 'deploy', 'ai'
    mensagem: str
    usuario_id: Optional[str] = None  # ID do usuário que realizou a ação
    detalhes: Optional[dict] = None  # Informações adicionais sobre o log

class LogQueryParams(BaseModel):
    """
    Representa os parâmetros de busca para filtragem de logs.
    """
    nivel: Optional[str] = None  # 'info', 'warning', 'error'
    origem: Optional[str] = None  # Filtra logs por origem específica
    usuario_id: Optional[str] = None  # Filtra logs por usuário específico
    data_inicio: Optional[datetime] = None  # Filtra logs a partir de uma data
    data_fim: Optional[datetime] = None  # Filtra logs até uma data específica
