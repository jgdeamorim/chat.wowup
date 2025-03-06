from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class MenuItem(BaseModel):
    """
    Representa um item do menu do frontend.
    """
    titulo: str
    icone: Optional[str] = None
    rota: str
    submenus: Optional[List["MenuItem"]] = []

class PageComponent(BaseModel):
    """
    Representa um componente dentro de uma página do frontend.
    """
    tipo: str  # Ex: "widget", "tabela", "formulario"
    descricao: Optional[str] = None

class PageModel(BaseModel):
    """
    Representa uma página do frontend.
    """
    nome: str
    rota: str
    componentes: List[PageComponent]
    ultima_atualizacao: datetime = datetime.utcnow()

class FrontendComponent(BaseModel):  # ✅ 🔹 Adicionado esta classe
    """
    Modelo para registrar um novo componente do frontend.
    """
    name: str
    description: Optional[str] = None
    route: str

class FrontendModel(BaseModel):
    """
    Modelo principal para armazenamento do frontend.
    """
    menus: List[MenuItem]
    paginas: List[PageModel]
    endpoints: List[dict]
    ultima_atualizacao: datetime = datetime.utcnow()

    class Config:
        schema_extra = {
            "example": {
                "menus": [
                    {
                        "titulo": "Dashboard",
                        "icone": "home",
                        "rota": "/dashboard"
                    },
                    {
                        "titulo": "Usuários",
                        "icone": "users",
                        "rota": "/users",
                        "submenus": [
                            {"titulo": "Gerenciar Usuários", "rota": "/users/manage"},
                            {"titulo": "Permissões", "rota": "/users/permissions"}
                        ]
                    }
                ],
                "paginas": [
                    {
                        "nome": "Dashboard",
                        "rota": "/dashboard",
                        "componentes": [
                            {"tipo": "widget", "descricao": "Resumo do sistema"},
                            {"tipo": "grafico", "descricao": "Gráfico de acessos"}
                        ]
                    }
                ],
                "endpoints": [
                    {"rota": "/api/v1/users", "metodo": "GET", "descricao": "Lista todos os usuários"},
                    {"rota": "/api/v1/users/{user_id}", "metodo": "DELETE", "descricao": "Remove um usuário"},
                    {"rota": "/api/v1/admin/configurations", "metodo": "GET", "descricao": "Obtém as configurações"}
                ],
                "ultima_atualizacao": "2025-03-05"
            }
        }
