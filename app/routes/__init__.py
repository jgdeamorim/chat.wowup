from fastapi import APIRouter

from .chat import router as chat_router
from .modules import router as modules_router
from .system import router as system_router
from .logs import router as logs_router
from .users import router as users_router

router = APIRouter()
router.include_router(chat_router, prefix="/chat", tags=["Chat Assistente"])
router.include_router(modules_router, prefix="/modules", tags=["Módulos"])
router.include_router(system_router, prefix="/system", tags=["Sistema"])
router.include_router(logs_router, prefix="/logs", tags=["Logs"])
router.include_router(users_router, prefix="/users", tags=["Usuários"])
