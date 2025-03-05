# app/services/versioning_service.py

from datetime import datetime
from app.core.database import get_database
from fastapi import HTTPException
from bson import ObjectId
from typing import Dict, Any

async def create_version(module_name: str, changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cria uma nova versão de um módulo, armazenando as alterações feitas.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    version_data = {
        "module_name": module_name,
        "changes": changes,
        "created_at": datetime.utcnow(),
        "status": "active"
    }

    result = await db["versioning"].insert_one(version_data)
    version_id = str(result.inserted_id)

    return {"message": f"Versão criada para o módulo '{module_name}'", "version_id": version_id}

async def get_version_history(module_name: str) -> Dict[str, Any]:
    """
    Retorna o histórico de versões de um módulo específico.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    versions = await db["versioning"].find({"module_name": module_name}).sort("created_at", -1).to_list(length=50)

    if not versions:
        raise HTTPException(status_code=404, detail=f"Nenhuma versão encontrada para o módulo '{module_name}'.")

    return {"module_name": module_name, "versions": versions}

async def rollback_version(version_id: str) -> Dict[str, Any]:
    """
    Reverte um módulo para uma versão específica.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    if not ObjectId.is_valid(version_id):
        raise HTTPException(status_code=400, detail="ID de versão inválido.")

    version_data = await db["versioning"].find_one({"_id": ObjectId(version_id)})
    if not version_data:
        raise HTTPException(status_code=404, detail=f"Versão '{version_id}' não encontrada.")

    # Atualizar status da versão revertida
    await db["versioning"].update_one({"_id": ObjectId(version_id)}, {"$set": {"status": "reverted"}})

    return {"message": f"Versão '{version_id}' revertida com sucesso!", "reverted_version": version_data}

async def compare_versions(version_id_1: str, version_id_2: str) -> Dict[str, Any]:
    """
    Compara duas versões do mesmo módulo e exibe as diferenças.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    if not ObjectId.is_valid(version_id_1) or not ObjectId.is_valid(version_id_2):
        raise HTTPException(status_code=400, detail="IDs de versão inválidos.")

    version_1 = await db["versioning"].find_one({"_id": ObjectId(version_id_1)})
    version_2 = await db["versioning"].find_one({"_id": ObjectId(version_id_2)})

    if not version_1 or not version_2:
        raise HTTPException(status_code=404, detail="Uma ou ambas as versões não foram encontradas.")

    differences = {
        key: {"versao_1": version_1["changes"].get(key), "versao_2": version_2["changes"].get(key)}
        for key in set(version_1["changes"]) | set(version_2["changes"])
        if version_1["changes"].get(key) != version_2["changes"].get(key)
    }

    return {
        "version_1": version_id_1,
        "version_2": version_id_2,
        "differences": differences
    }
