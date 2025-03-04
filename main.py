from fastapi import FastAPI
from app.core.database import init_db
from app.routes import (
    chat,
    modules,
    system,
    logs,
    users,
    frontend_sync
)
from config.settings import settings  # Se settings.py estiver fora da pasta app

import os
import sys
import logging
from datetime import datetime

# 🔹 Ajuste no PYTHONPATH para evitar importações quebradas (remova se usar Docker)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Chat Central - Assistente Inteligente para Gestão de Projetos e Módulos"
)

# Inicializa a conexão com o banco de dados ao iniciar a API
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("🔹 Iniciando conexão com o banco de dados...")
        await init_db()
        logger.info("✅ Conexão com o banco de dados estabelecida com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao conectar ao banco de dados: {e}")

# Garante o encerramento correto das conexões ao desligar o sistema
@app.on_event("shutdown")
async def shutdown_event():
    logger.warning("⚠️ Encerrando conexões do banco de dados...")

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
    Verifica o status do sistema, incluindo o banco de dados e o Redis.
    """
    health_data = {
        "status": "Online",
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Testa conexão com o banco de dados
    try:
        db_status = await init_db()  # Aqui pode ser ajustado conforme a estrutura do `init_db`
        health_data["database"] = "✅ Conectado"
    except Exception:
        health_data["database"] = "❌ Erro na conexão"

    return health_data
