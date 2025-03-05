# app/services/module_manager.py

from datetime import datetime
from app.core.database import get_database
from bson import ObjectId

db = get_database()

async def create_module(module_name: str, module_type: str = "internal", description: str = "Módulo criado pelo Chat Central"):
    """
    Cria um novo módulo e salva no banco de dados.
    """
    existing_module = await db["modules"].find_one({"name": module_name})
    if existing_module:
        return {"error": f"O módulo '{module_name}' já existe."}

    module_data = {
        "name": module_name,
        "type": module_type,
        "description": description,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "versions": []
    }

    await db["modules"].insert_one(module_data)
    return {"message": f"Módulo '{module_name}' criado com sucesso!", "module": module_data}

async def update_module(module_name: str, updates: dict):
    """
    Atualiza um módulo existente.
    """
    module = await db["modules"].find_one({"name": module_name})
    if not module:
        return {"error": f"Módulo '{module_name}' não encontrado."}

    updates["updated_at"] = datetime.utcnow()
    await db["modules"].update_one({"name": module_name}, {"$set": updates})
    return {"message": f"Módulo '{module_name}' atualizado!", "updated_fields": updates}

async def delete_module(module_name: str):
    """
    Remove um módulo do sistema, garantindo que ele não tenha dependências ativas.
    """
    dependencies = await db["modules"].find({"parent_module": module_name}).to_list(None)
    if dependencies:
        return {"error": f"O módulo '{module_name}' possui dependências e não pode ser excluído."}

    result = await db["modules"].delete_one({"name": module_name})
    if result.deleted_count == 0:
        return {"error": f"Módulo '{module_name}' não encontrado."}

    return {"message": f"Módulo '{module_name}' removido com sucesso!"}
