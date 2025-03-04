# app/models/project_model.py

from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class ProjectModule(BaseModel):
    """
    Representa um módulo utilizado dentro de um projeto.
    """
    modulo_nome: str
    versao_utilizada: Optional[str] = None  # Exemplo: "v1.0"

class ProjectVersion(BaseModel):
    """
    Representa uma versão específica de um projeto.
    """
    versao: str
    data_criacao: datetime = datetime.utcnow()
    alteracoes: Optional[str] = None  # Descrição das mudanças

class ProjectEntry(BaseModel):
    """
    Representa um projeto gerenciado pelo Chat Central.
    """
    nome: str
    descricao: Optional[str] = None
    status: str  # Exemplo: "ativo", "arquivado", "em desenvolvimento"
    versao_atual: str
    historico_versoes: List[ProjectVersion] = []
    modulos_utilizados: List[ProjectModule] = []
    ultima_modificacao: datetime = datetime.utcnow()
    gerenciado_por_ia: bool = False  # Se a IA está gerenciando o projeto
