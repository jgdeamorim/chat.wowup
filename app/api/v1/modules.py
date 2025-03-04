# Caminho: app/api/v1/modules.py

from fastapi import APIRouter, HTTPException, Depends
from app.services.module_manager import (
    create_module, update_module, delete_module, optimize_module, get_module_dependencies
)
from app.core.database import get_database
from datetime import datetime

router = APIRouter()
db = get_database()

@router.get("/")
async def list_modules():
    """
    Lista todos os módulos disponíveis no sistema.
    """
    modules = await db["modules"].find().sort("created_at", -1).to_list(length=50)
    return {"modules": modules}

@router.get("/{module_name}")
async def get_module_details(module_name: str):
    """
    Retorna detalhes sobre um módulo específico.
    """
    module = await db["modules"].find_one({"name": module_name})
    if not module:
        raise HTTPException(status_code=404, detail=f"Módulo '{module_name}' não encontrado.")
    return {"module": module}

@router.post("/create")
async def create_new_module(request: dict):
    """
    Cria um novo módulo interno ou externo, verificando se já existe um módulo com o mesmo nome.
    """
    module_name = request.get("module_name", "").strip()
    if not module_name:
        raise HTTPException(status_code=400, detail="O nome do módulo não pode estar vazio.")

    # Verificar se já existe um módulo com esse nome
    existing_module = await db["modules"].find_one({"name": module_name})
    if existing_module:
        raise HTTPException(status_code=400, detail="Já existe um módulo com esse nome.")

    module_type = request.get("module_type", "internal")  # internal | external
    description = request.get("description", "Módulo gerado pelo Chat Central")
    
    result = await create_module(module_name, module_type, description)

    return {"message": f"Módulo '{module_name}' criado com sucesso!", "details": result}

@router.put("/update/{module_name}")
async def update_existing_module(module_name: str, request: dict):
    """
    Modifica um módulo existente, garantindo versionamento e rastreabilidade das mudanças.
    """
    updates = request.get("updates", {})
    if not updates:
        raise HTTPException(status_code=400, detail="Nenhuma atualização fornecida.")

    result = await update_module(module_name, updates)

    # Registrar versão da atualização
    version_data = {
        "module_name": module_name,
        "updates": updates,
        "timestamp": datetime.utcnow()
    }
    await db["module_versions"].insert_one(version_data)

    return {"message": f"Módulo '{module_name}' atualizado!", "details": result}

@router.delete("/delete/{module_name}")
async def delete_existing_module(module_name: str):
    """
    Remove um módulo do sistema, garantindo que ele não tenha dependências ativas antes da exclusão.
    """
    dependencies = await get_module_dependencies(module_name)
    if dependencies:
        raise HTTPException(status_code=400, detail=f"O módulo '{module_name}' possui dependências e não pode ser excluído.")

    result = await delete_module(module_name)
    
    return {"message": f"Módulo '{module_name}' removido com sucesso!", "details": result}

@router.post("/optimize/{module_name}")
async def optimize_existing_module(module_name: str):
    """
    A IA analisa e melhora um módulo automaticamente.
    """
    result = await optimize_module(module_name)
    return {"message": f"Módulo '{module_name}' otimizado!", "details": result}

@router.get("/dependencies/{module_name}")
async def get_module_dependency_list(module_name: str):
    """
    Retorna a lista de dependências de um módulo específico.
    """
    dependencies = await get_module_dependencies(module_name)
    return {"module": module_name, "dependencies": dependencies}
