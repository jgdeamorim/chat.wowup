from fastapi import FastAPI
from app.core.database import database
from app.routes import (
    chat,
    modules,
    system,
    logs,
    users,
    frontend_sync
)
from config.settings import settings  # Garante que `settings.py` esteja corretamente referenciado

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

# Garante o encerramento correto das conexões ao desligar o sistema
@app.on_event("shutdown")
async def shutdown_event():
    logger.warning("⚠️ Encerrando conexões do banco de dados...")
    await database.client.close()

# Inclui as rotas principais da API
app.include_router(chat.router, prefix="/chat", tags=["Chat Assistente"])
app.include_router(modules.router, prefix="/modules", tags=["Módulos Internos"])
app.include_router(system.router, prefix="/system", tags=["Controle do Sistema"])
app.include_router(logs.router, prefix="/logs", tags=["Monitoramento"])
app.include_router(users.router, prefix="/users", tags=["Usuários e Permissões"])
app.include_router(frontend_sync.router, prefix="/frontend", tags=["Sincronização Frontend"])

# Endpoint de status do sistema
@app.get("/")
async def health_check():
    """
    Verifica o status do sistema, incluindo o banco de dados.
    """
    health_data = {
        "status": "Online",
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Testa conexão com o banco de dados sem reinicializar `init_db()`
    try:
        if database.client:
            health_data["database"] = "✅ Conectado"
        else:
            health_data["database"] = "❌ Erro na conexão"
    except Exception:
        health_data["database"] = "❌ Erro na conexão"

    return health_data

# Ponto de entrada para rodar o servidor Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

