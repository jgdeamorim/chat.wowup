import logging
import motor.motor_asyncio
import redis.asyncio as redis
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logs
logger = logging.getLogger("database")
logger.setLevel(logging.INFO)

# Configuração do MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ia-dev")
MONGO_TIMEOUT_MS = int(os.getenv("MONGO_TIMEOUT_MS", 5000))  # Timeout de 5 segundos

# Configuração do Redis
REDIS_URI = os.getenv("REDIS_URI")

# Verificação das variáveis de ambiente
if not MONGO_URI:
    raise ValueError("❌ ERRO: A variável 'MONGO_URI' não está configurada. Configure no Railway.")

if not REDIS_URI:
    raise ValueError("❌ ERRO: A variável 'REDIS_URI' não está configurada. Configure no Railway.")

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
            if self.client is None:
                logger.info("🔹 Conectando ao MongoDB...")
                self.client = motor.motor_asyncio.AsyncIOMotorClient(
                    MONGO_URI, serverSelectionTimeoutMS=MONGO_TIMEOUT_MS
                )
                self.db = self.client[DATABASE_NAME]
                await self.db.command("ping")  # Testa conexão
                logger.info("✅ Conectado ao MongoDB com sucesso.")

            if self.redis is None:
                logger.info("🔹 Conectando ao Redis...")
                self.redis = redis.Redis.from_url(REDIS_URI, decode_responses=True)
                if await self.redis.ping():
                    logger.info("✅ Conectado ao Redis com sucesso.")
                else:
                    logger.error("❌ Falha ao conectar ao Redis.")
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao banco de dados: {str(e)}")
            raise e

    async def get_database(self):
        """
        Retorna a conexão ativa com o MongoDB.
        """
        if self.client is None:
            logger.warning("⚠️ Nenhuma conexão ativa com MongoDB. Tentando reconectar...")
            await self.connect()

        if self.db is None:
            raise ConnectionError("❌ Erro: Banco de dados não disponível após reconexão!")

        return self.db

    async def get_redis(self):
        """
        Retorna a conexão ativa com o Redis.
        """
        if self.redis is None:
            logger.warning("⚠️ Nenhuma conexão ativa com Redis. Tentando reconectar...")
            await self.connect()

        if self.redis is None:
            raise ConnectionError("❌ Erro: Redis não disponível após reconexão!")

        return self.redis

# Instância global do banco de dados
database = Database()

async def get_database():
    """
    Função global para obter a conexão ativa do MongoDB.
    """
    return await database.get_database()

async def get_redis():
    """
    Função global para obter a conexão ativa do Redis.
    """
    return await database.get_redis()
