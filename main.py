from fastapi import FastAPI
from app.core.database import init_db
from app.api.v1 import chat, modules, system, logs, users, frontend_sync
from config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Chat Central - Assistente Inteligente para Gestão de Projetos e Módulos"
)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(chat.router, prefix="/chat", tags=["Chat Assistente"])
app.include_router(modules.router, prefix="/modules", tags=["Módulos Internos"])
app.include_router(system.router, prefix="/system", tags=["Controle do Sistema"])
app.include_router(logs.router, prefix="/logs", tags=["Monitoramento"])
app.include_router(users.router, prefix="/users", tags=["Usuários e Permissões"])
app.include_router(frontend_sync.router, prefix="/frontend", tags=["Sincronização Frontend"])

@app.get("/")
async def health_check():
    return {"status": "Online", "version": settings.VERSION}
