# app/services/uiux_tuner.py

from app.core.database import get_database

async def analyze_uiux():
    """
    Verifica padrões de interface e sugere melhorias de UI/UX.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    ui_suggestions = []

    # Avaliação da estrutura do frontend
    current_ui = await db["frontend_settings"].find_one({"active_theme": {"$exists": True}})

    if current_ui and current_ui["active_theme"] == "default":
        ui_suggestions.append("🎨 Alterar para um tema mais moderno com suporte a dark mode.")

    return {"response": "Análise de UI/UX concluída!", "suggestions": ui_suggestions}

async def apply_ui_fixes():
    """
    Aplica automaticamente as melhorias sugeridas para UI/UX.
    """
    db = await get_database()  # 🔹 Correção: Adicionado `await get_database()`
    
    await db["frontend_settings"].update_one({}, {"$set": {"active_theme": "modern"}})
    return {"response": "Tema atualizado para 'modern' e otimizações aplicadas!"}
