# app/models/tuning_model.py

from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class FineTuningEntry(BaseModel):
    """
    Representa um ajuste fino aplicado pela IA no sistema.
    """
    modulo_afetado: str  # Exemplo: "Autenticação", "Banco de Dados", "Frontend"
    tipo_ajuste: str  # Exemplo: "Segurança", "Performance", "UI/UX"
    descricao: str  # Explicação da melhoria aplicada
    data_aplicacao: datetime = datetime.utcnow()
    versao_antes: Optional[str] = None  # Versão antes do ajuste
    versao_depois: Optional[str] = None  # Versão após o ajuste
    aplicado_por_ia: bool = True  # Define se foi um ajuste automático ou manual
    rollback_disponivel: bool = False  # Define se é possível reverter a alteração

class IAPersonalization(BaseModel):
    """
    Define as preferências do Admin para otimizações da IA.
    """
    nivel_controle: str  # Exemplo: "Baixo", "Médio", "Alto", "Controle Total IA"
    priorizar_performance: bool = False
    priorizar_seguranca: bool = True
    priorizar_ui_ux: bool = False
    historico_ajustes: list[FineTuningEntry] = []  # Histórico de otimizações feitas pela IA
