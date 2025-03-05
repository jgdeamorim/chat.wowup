from fastapi import APIRouter, HTTPException, Depends
from app.services.chat_assistant import process_chat_request, create_module, improve_module, fetch_ai_suggestions
from app.core.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from typing import Dict, Any

router = APIRouter()

@router.post("/message")
async def chat_with_ai(request: Dict[str, Any], db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Envia uma mensagem para a IA e recebe uma resposta inteligente baseada no aprendizado contínuo.
    """
    try:
        user_message = request.get("message", "").strip()
        if not user_message:
            raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")

        response = await process_chat_request(db, user_message)

        # Salvar no histórico do chat
        chat_log = {
            "timestamp": datetime.utcnow(),
            "user_message": user_message,
            "ai_response": response
        }
        await db["chat_history"].insert_one(chat_log)

        return {"response": response}
    except Exception as e:
        return {"error": f"Erro no processamento do chat: {str(e)}"}

@router.get("/history")
async def get_chat_history(limit: int = 50, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Retorna o histórico de interações do Admin com o Chat Central.
    """
    try:
        chat_logs = await db["chat_history"].find().sort("timestamp", -1).limit(limit).to_list(length=limit)
        return {"history": chat_logs if chat_logs else "Nenhum histórico encontrado."}
    except Exception as e:
        return {"error": f"Erro ao recuperar histórico do chat: {str(e)}"}

@router.post("/create-module")
async def create_internal_module(request: Dict[str, Any], db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    O Admin solicita a criação de um novo módulo interno no sistema via Chat Assistente.
    """
    try:
        module_name = request.get("module_name", "").strip()
        if not module_name:
            raise HTTPException(status_code=400, detail="O nome do módulo não pode estar vazio.")

        result = await create_module(db, module_name)
        return {"message": f"Módulo '{module_name}' criado com sucesso!", "details": result}
    except Exception as e:
        return {"error": f"Erro ao criar módulo: {str(e)}"}

@router.post("/improve-module")
async def improve_existing_module(request: Dict[str, Any], db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    O Admin solicita melhorias para um módulo existente.
    """
    try:
        module_name = request.get("module_name", "").strip()
        if not module_name:
            raise HTTPException(status_code=400, detail="O nome do módulo não pode estar vazio.")

        result = await improve_module(db, module_name)
        return {"message": f"Módulo '{module_name}' aprimorado!", "details": result}
    except Exception as e:
        return {"error": f"Erro ao melhorar módulo: {str(e)}"}

@router.get("/suggestions")
async def get_ai_suggestions(limit: int = 10, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Retorna sugestões de melhorias baseadas no aprendizado contínuo da IA.
    """
    try:
        suggestions = await fetch_ai_suggestions(db, limit)
        return {"suggestions": suggestions if suggestions else "Nenhuma sugestão disponível."}
    except Exception as e:
        return {"error": f"Erro ao recuperar sugestões da IA: {str(e)}"}
