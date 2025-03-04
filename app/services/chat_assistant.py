# app/services/chat_assistant.py

from datetime import datetime
from app.core.database import get_database
from app.services.module_manager import create_module
from app.services.fine_tuning_manager import apply_fine_tuning
from typing import Dict, Any

db = get_database()

async def process_chat_request(user_message: str) -> Dict[str, Any]:
    """
    Processa a mensagem do Admin e retorna uma resposta da IA baseada no contexto.
    """
    response = {}
    
    # Histórico para aprendizado contínuo
    chat_log = {
        "timestamp": datetime.utcnow(),
        "user_message": user_message
    }
    
    # Analisando a intenção da mensagem
    if "criar módulo" in user_message.lower():
        module_name = extract_module_name(user_message)
        existing_module = await db["modules"].find_one({"name": module_name})

        if existing_module:
            response["message"] = f"O módulo '{module_name}' já existe. Deseja aprimorá-lo?"
        else:
            new_module = await create_module(module_name)
            response["message"] = f"Módulo '{module_name}' criado com sucesso!"
            response["details"] = new_module

    elif "otimizar sistema" in user_message.lower():
        optimization_result = await apply_fine_tuning()
        response["message"] = "Otimizações aplicadas com sucesso!"
        response["details"] = optimization_result

    else:
        response["message"] = "Desculpe, não entendi sua solicitação. Poderia reformular?"

    # Salvando no histórico do chat
    chat_log["ai_response"] = response
    await db["chat_history"].insert_one(chat_log)

    return response

def extract_module_name(user_message: str) -> str:
    """
    Extrai o nome do módulo da mensagem do Admin.
    """
    words = user_message.split()
    if "módulo" in words:
        index = words.index("módulo") + 1
        return words[index] if index < len(words) else "Modulo_Desconhecido"
    return "Modulo_Desconhecido"
