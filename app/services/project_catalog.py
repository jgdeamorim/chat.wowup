# app/services/project_catalog.py

from app.core.database import get_database
from app.models.project_model import Project

db = get_database()

async def catalog_project():
    """
    Gera um relatório sobre os módulos existentes, APIs e banco de dados.
    """
    modules = await db["modules"].find().to_list(None)
    database_collections = await db.list_collection_names()

    project_data = {
        "total_modules": len(modules),
        "modules": [mod["name"] for mod in modules],
        "database_collections": database_collections
    }

    return {"response": "Catálogo do projeto atualizado!", "data": project_data}
