# app/routes/modules.py

from fastapi import APIRouter, HTTPException
from app.core.database import get_database
from app.models.module_model import Module
from app.services.versioning_service import version_project

router = APIRouter()
db = get_database()

@router.post("/create")
async def create_module(module: Module):
    """
    Cria um novo módulo e registra no banco de dados.
    """
    existing_module = await db["modules"].find_one({"name": module.name})
    if existing_module:
        raise HTTPException(status_code=400, detail="Módulo já existe.")

    await db["modules"].insert_one(module.dict())
    version_project(module.name, "Criado novo módulo")
    
    return {"response": f"Módulo {module.name} criado com sucesso!"}

@router.put("/update/{module_name}")
async def update_module(module_name: str, update_data: dict):
    """
    Atualiza um módulo existente com novas configurações.
    """
    module = await db["modules"].find_one({"name": module_name})
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado.")

    await db["modules"].update_one({"name": module_name}, {"$set": update_data})
    version_project(module_name, "Atualizado módulo")

    return {"response": f"Módulo {module_name} atualizado!"}

@router.delete("/delete/{module_name}")
async def delete_module(module_name: str):
    """
    Remove um módulo do sistema.
    """
    module = await db["modules"].find_one({"name": module_name})
    if not module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado.")

    await db["modules"].delete_one({"name": module_name})
    return {"response": f"Módulo {module_name} removido!"}
