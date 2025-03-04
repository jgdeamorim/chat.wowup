# app/core/database.py

import logging
import motor.motor_asyncio
import aioredis
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logs
logger = logging.getLogger("database")
logger.setLevel(logging.INFO)

# Configurações do MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://crossover.proxy.rlwy.net:52597")
DATABASE_NAME = os.getenv("DATABASE_NAME", "chat_central")

# Configurações do Redis
REDIS_URI = os.getenv("REDIS_URI", "redis://maglev.proxy.rlwy.net:17929")

# Inicializa clientes de banco de dados
class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.redis = None

    async def connect(self):
        """
        Conecta ao MongoDB e Redis, garantindo a disponibilidade do banco de dados.
        """
        try:
            # Conectar ao MongoDB
            self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
            self.db = self.client[DATABASE_NAME]
            logger.info("✅ Conectado ao MongoDB com sucesso.")

            # Conectar ao Redis
            self.redis = await aioredis.from_url(REDIS_URI, decode_responses=True)
            logger.info("✅ Conectado ao Redis com sucesso.")

        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao banco de dados: {e}")
            raise e

    async def disconnect(self):
        """
        Fecha as conexões com MongoDB e Redis quando o sistema for desligado.
        """
        if self.client:
            self.client.close()
            logger.info("🔌 Conexão com MongoDB fechada.")

        if self.redis:
            await self.redis.close()
            logger.info("🔌 Conexão com Redis fechada.")

    async def check_connection(self):
        """
        Verifica se as conexões com MongoDB e Redis estão ativas e, se necessário, tenta reconectar.
        """
        try:
            # Testa conexão com MongoDB
            await self.db.command("ping")
            logger.info("✅ MongoDB está online.")

            # Testa conexão com Redis
            pong = await self.redis.ping()
            if pong:
                logger.info("✅ Redis está online.")

        except Exception:
            logger.warning("⚠️ Conexão perdida. Tentando reconectar...")
            await self.connect()

    async def get_database(self):
        """
        Retorna a conexão ativa com o banco de dados.
        """
        if not self.db:
            await self.connect()
        return self.db

    async def get_redis(self):
        """
        Retorna a conexão ativa com o Redis.
        """
        if not self.redis:
            await self.connect()
        return self.redis

# Instância global do banco de dados
database = Database()

async def get_database():
    return await database.get_database()

async def get_redis():
    return await database.get_redis()
