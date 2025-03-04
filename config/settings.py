# config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Chat Central"
    VERSION: str = "1.20"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Configuração do Banco de Dados
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/chatcentral")
    REDIS_URI: str = os.getenv("REDIS_URI", "redis://localhost:6379")

    # Segurança e Autenticação
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Configuração da IA
    AI_ENGINE: str = os.getenv("AI_ENGINE", "openai-gpt4o")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

settings = Settings()
