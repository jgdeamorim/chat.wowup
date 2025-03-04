# config/settings.py

import os
from dotenv import load_dotenv
import secrets

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Chat Central"
    VERSION: str = "1.20"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Configuração do Banco de Dados
    MONGO_URI: str = os.getenv("MONGO_URI")
    REDIS_URI: str = os.getenv("REDIS_URI")

    if not MONGO_URI or not REDIS_URI:
        raise ValueError("As variáveis de ambiente MONGO_URI e REDIS_URI precisam estar definidas!")

    # Segurança e Autenticação
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    if not JWT_SECRET_KEY:
        raise ValueError("A variável de ambiente JWT_SECRET_KEY não foi definida!")

    # Configuração da IA
    AI_ENGINE: str = os.getenv("AI_ENGINE", "gpt4o")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    if not OPENAI_API_KEY:
        raise ValueError("A variável de ambiente OPENAI_API_KEY não foi definida!")

settings = Settings()
