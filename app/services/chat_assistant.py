# app/services/chat_assistant.py

from datetime import datetime
from app.core.database import get_database
from app.services.module_manager import create_module
from app.services.fine_tuning_manager import apply_fine_tuning
from typing import Dict, Any

async def process_chat_request(user_message: str) -> Dict[str, Any]:
    """
    Processa a mensagem do Admin e retorna uma resposta da IA baseada no contexto.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    response = {}
    
    # Histórico para aprendizado contínuo
    chat_log = {
        "timestamp": datetime.utcnow(),
        "user_message": user_message
    }
    
    try:
        # Analisando a intenção da mensagem
        user_message_lower = user_message.lower()

        if "criar módulo" in user_message_lower or "novo módulo" in user_message_lower:
            module_name = extract_module_name(user_message)
            if not module_name or module_name == "Modulo_Desconhecido":
                response["message"] = "Por favor, especifique o nome do módulo que deseja criar."
            else:
                existing_module = await db["modules"].find_one({"name": module_name})

                if existing_module:
                    response["message"] = f"O módulo '{module_name}' já existe. Deseja aprimorá-lo?"
                else:
                    new_module = await create_module(module_name)  # 🔹 Correção: Agora `await`
                    response["message"] = f"Módulo '{module_name}' criado com sucesso!"
                    response["details"] = new_module

        elif "otimizar sistema" in user_message_lower or "melhorar desempenho" in user_message_lower:
            optimization_result = await apply_fine_tuning()  # 🔹 Correção: Agora `await`
            response["message"] = "Otimizações aplicadas com sucesso!"
            response["details"] = optimization_result

        else:
            response["message"] = "Desculpe, não entendi sua solicitação. Poderia reformular?"

        # Salvando no histórico do chat
        chat_log["ai_response"] = response
        await db["chat_history"].insert_one(chat_log)

    except Exception as e:
        response["message"] = f"Erro ao processar a solicitação: {str(e)}"
    
    return response

def extract_module_name(user_message: str) -> str:
    """
    Extrai o nome do módulo da mensagem do Admin de forma mais robusta.
    """
    words = user_message.split()
    if "módulo" in words:
        index = words.index("módulo") + 1
        if index < len(words):
            return words[index].strip(".,!?").capitalize()
    return "Modulo_Desconhecido"
