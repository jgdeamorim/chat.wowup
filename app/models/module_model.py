# app/models/module_model.py

from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class ModuleDependency(BaseModel):
    """
    Representa uma dependência de um módulo para outro.
    """
    modulo_nome: str
    versao_requerida: Optional[str] = None  # Exemplo: "v1.0"

class ModuleVersion(BaseModel):
    """
    Representa uma versão específica de um módulo.
    """
    versao: str
    data_criacao: datetime = datetime.utcnow()
    alteracoes: Optional[str] = None  # Descrição das mudanças

class ModuleEntry(BaseModel):
    """
    Representa um módulo no sistema.
    """
    nome: str
    tipo: str  # Exemplo: "interno", "externo"
    descricao: Optional[str] = None
    status: str  # Exemplo: "ativo", "desativado", "em desenvolvimento"
    versao_atual: str
    historico_versoes: List[ModuleVersion] = []
    dependencias: List[ModuleDependency] = []
    otimizado_por_ia: bool = False  # Se já recebeu otimização automatizada
    ultima_modificacao: datetime = datetime.utcnow()
