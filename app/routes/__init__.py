from fastapi import APIRouter

from .chat import router as chat_router
from .modules import router as modules_router
from .system import router as system_router
from .logs import router as logs_router
from .users import router as users_router
from .frontend_sync import router as frontend_sync_router

router = APIRouter()
router.include_router(chat_router, prefix="/chat", tags=["Chat Assistente"])
router.include_router(modules_router, prefix="/modules", tags=["Módulos Internos"])
router.include_router(system_router, prefix="/system", tags=["Controle do Sistema"])
router.include_router(logs_router, prefix="/logs", tags=["Monitoramento"])
router.include_router(users_router, prefix="/users", tags=["Usuários"])
router.include_router(frontend_sync_router, prefix="/frontend", tags=["Sincronização Frontend"])
