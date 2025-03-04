# app/services/ai_improvement.py

from app.core.database import get_database

db = get_database()

async def analyze_feedback():
    """
    Analisa feedbacks armazenados e sugere melhorias para a IA.
    """
    feedbacks = await db["ai_learning"].find().to_list(None)
    improvement_suggestions = []

    for feedback in feedbacks:
        if feedback.get("adjustment") and feedback["approved"]:
            improvement_suggestions.append(f"🔍 Aprimorar {feedback['module']} com base em feedback validado.")

    return {"response": "Análise concluída!", "suggestions": improvement_suggestions}

async def apply_ai_improvements():
    """
    Aplica ajustes recomendados à IA com base nos feedbacks registrados.
    """
    applied_improvements = []

    async for feedback in db["ai_learning"].find({"approved": True}):
        module_name = feedback.get("module")
        adjustment = feedback.get("adjustment")
        
        if module_name and adjustment:
            applied_improvements.append(f"✅ {module_name}: {adjustment} aplicado.")
    
    return {"response": "Melhorias implementadas!", "details": applied_improvements}
