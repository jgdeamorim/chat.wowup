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
from datetime import datetime

# 🔹 Ajuste no PYTHONPATH para evitar importações quebradas (remova se usar Docker)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Chat Central - Assistente Inteligente para Gestão de Projetos e Módulos"
)

# Inicializa a conexão com o banco de dados ao iniciar a API
@app.on_event("startup")
async def startup_event():
    try:
        await init_db()
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")

# Garante o encerramento correto das conexões ao desligar o sistema
@app.on_event("shutdown")
async def shutdown_event():
    print("⚠️ Encerrando conexões do banco de dados...")

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
    return {
        "status": "Online",
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }
