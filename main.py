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
from config.settings import settings  # Importação garantida

import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialização do FastAPI
app = FastAPI(
    title=getattr(settings, "PROJECT_NAME", "Chat Central API"),
    version=getattr(settings, "VERSION", "1.0.0"),
    description="Chat Central - Assistente Inteligente para Gestão de Projetos e Módulos"
)

# 🔹 Evento de startup: Conexão com MongoDB e Redis
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("🔹 Iniciando conexão com o banco de dados...")
        await database.connect()
        logger.info("✅ Conexão com o banco de dados estabelecida com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao conectar ao banco de dados: {e}")

# 🔹 Evento de shutdown: Fecha conexões com MongoDB e Redis corretamente
@app.on_event("shutdown")
async def shutdown_event():
    try:
        logger.warning("⚠️ Encerrando conexões do banco de dados...")
        await database.disconnect()
        logger.info("🔌 Conexões encerradas com sucesso.")
    except Exception as e:
        logger.error(f"❌ Erro ao encerrar conexões: {e}")

# 🔹 Inclui as rotas principais da API
app.include_router(chat.router, prefix="/api//chat", tags=["Chat Assistente"])
app.include_router(modules.router, prefix="/api/modules", tags=["Módulos Internos"])
app.include_router(system.router, prefix="/api/system", tags=["Controle do Sistema"])
app.include_router(logs.router, prefix="/api/logs", tags=["Monitoramento"])
app.include_router(users.router, prefix="/api/users", tags=["Usuários e Permissões"])
app.include_router(frontend_sync.router, prefix="/api/frontend-sync", tags=["Sincronização Frontend"])

# 🔹 Health Check - Verifica status da API e conexões do banco
@app.get("/")
async def health_check():
    """
    Verifica o status do sistema e a conexão com o banco de dados.
    """
    health_data = {
        "status": "Online",
        "version": getattr(settings, "VERSION", "1.0.0"),
        "timestamp": datetime.utcnow().isoformat(),
        "database": "⏳ Verificando...",
        "redis": "⏳ Verificando..."
    }

    try:
        if database.client:
            await database.db.command("ping")  # Testa conexão MongoDB
            health_data["database"] = "✅ Conectado"
        else:
            health_data["database"] = "❌ Erro na conexão"
    except Exception:
        health_data["database"] = "❌ Erro na conexão"

    try:
        redis_conn = await database.get_redis()
        if await redis_conn.ping():
            health_data["redis"] = "✅ Conectado"
        else:
            health_data["redis"] = "❌ Erro na conexão"
    except Exception:
        health_data["redis"] = "❌ Erro na conexão"

    return health_data

# 🔹 Inicia o servidor Uvicorn quando executado diretamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
