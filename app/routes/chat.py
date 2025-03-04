# Caminho: app/routes/chat.py

from fastapi import APIRouter, HTTPException
from app.services.chat_assistant import process_chat_request
from datetime import datetime
from typing import Dict, Any

router = APIRouter()

@router.post("/message")
async def chat_with_ai(request: Dict[str, Any]):
    """Permite que o Admin envie mensagens para o Chat Assistente e receba respostas da IA."""
    user_message = request.get("message", "").strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")

    response = await process_chat_request(user_message)

    return {"response": response, "timestamp": datetime.utcnow()}
