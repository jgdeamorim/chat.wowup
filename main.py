import sys
import os

# Adiciona o diretório raiz ao `sys.path`
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.core.database import init_db
from app.api.routes import chat, modules, system, logs, users, frontend_sync
from config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Chat Central - Assistente Inteligente para Gestão de Projetos e Módulos"
)
