from fastapi import FastAPI
from app.routes import users  # Confirme se está importando corretamente
from app.core.database import database
from config.settings import settings

import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialização do FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Chat Central - Assistente Inteligente para Gestão de Projetos e Módulos"
)

# Conectar ao banco de dados ao iniciar a aplicação
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("🔹 Iniciando conexão com o banco de dados...")
        await database.connect()
        logger.info("✅ Conexão com o banco de dados estabelecida com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao conectar ao banco de dados: {e}")

# Fechar conexões ao desligar a API
@app.on_event("shutdown")
async def shutdown_event():
    logger.warning("⚠️ Encerrando conexões do banco de dados...")
    await database.client.close()

# 📌 Certifique-se de que a linha abaixo está presente e correta:
app.include_router(users.router, prefix="/users", tags=["Usuários"])  # <-- Adicione essa linha!

# Endpoint de status do sistema
@app.get("/")
async def health_check():
    """
    Verifica o status do sistema.
    """
    return {
        "status": "Online",
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "database": "✅ Conectado" if database.client else "❌ Erro na conexão"
    }

# Rodar a API com Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
