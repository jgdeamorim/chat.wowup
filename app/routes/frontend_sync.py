# app/routes/frontend_sync.py

from fastapi import APIRouter, HTTPException
from app.core.database import get_database
from app.models.frontend_model import FrontendComponent

router = APIRouter()
db = get_database()

@router.get("/sync")
async def sync_frontend():
    """
    Retorna os componentes do frontend com base nos módulos existentes.
    """
    modules = await db["modules"].find().to_list(None)
    frontend_components = [{"name": mod["name"], "route": f"/{mod['name'].lower()}"} for mod in modules]

    return {"response": "Sincronização concluída!", "components": frontend_components}

@router.post("/register-component")
async def register_component(component: FrontendComponent):
    """
    Registra um novo componente do frontend.
    """
    existing_component = await db["frontend"].find_one({"name": component.name})
    if existing_component:
        raise HTTPException(status_code=400, detail="Componente já registrado.")

    await db["frontend"].insert_one(component.dict())
    return {"response": f"Componente {component.name} registrado com sucesso!"}
