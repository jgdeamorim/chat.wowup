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

# Verificar se a URI do MongoDB está configurada corretamente
if not MONGO_URI:
    raise ValueError("❌ ERRO: A variável 'MONGO_URI' não está configurada. Configure no Railway.")

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
            if not self.client:
                logger.info("🔹 Conectando ao MongoDB...")
                self.client = motor.motor_asyncio.AsyncIOMotorClient(
                    MONGO_URI, serverSelectionTimeoutMS=MONGO_TIMEOUT_MS
                )
                self.db = self.client[DATABASE_NAME]

                # Testa conexão com MongoDB
                if await self.db.command("ping"):
                    logger.info("✅ Conectado ao MongoDB com sucesso.")

            if not self.redis:
                logger.info("🔹 Conectando ao Redis...")
                self.redis = redis.Redis.from_url(REDIS_URI, decode_responses=True)
                
                # Testa conexão com Redis
                if await self.redis.ping():
                    logger.info("✅ Conectado ao Redis com sucesso.")
                else:
                    logger.error("❌ Falha ao conectar ao Redis.")
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao banco de dados: {str(e)}")
            raise e

    async def disconnect(self):
        """
        Fecha as conexões com MongoDB e Redis quando o sistema for desligado.
        """
        try:
            if self.client:
                self.client.close()  # ❗️ Corrigido: `close()` não é assíncrono
                logger.info("🔌 Conexão com MongoDB fechada.")

            if self.redis:
                await self.redis.close()
                logger.info("🔌 Conexão com Redis fechada.")

        except Exception as e:
            logger.error(f"❌ Erro ao fechar conexões: {str(e)}")

    async def check_connection(self):
        """
        Verifica se as conexões com MongoDB e Redis estão ativas e, se necessário, tenta reconectar.
        """
        try:
            if self.db:
                try:
                    if await self.db.command("ping"):
                        logger.info("✅ MongoDB está online.")
                except Exception:
                    logger.warning("⚠️ Conexão com MongoDB perdida. Tentando reconectar...")
                    await self.connect()

            if self.redis:
                if await self.redis.ping():
                    logger.info("✅ Redis está online.")
                else:
                    logger.warning("⚠️ Conexão com Redis perdida. Tentando reconectar...")
                    await self.connect()

        except Exception as e:
            logger.error(f"❌ Erro na verificação da conexão: {str(e)}")
            await self.connect()

    async def get_database(self):
        """
        Retorna a conexão ativa com o banco de dados.
        """
        if not self.client or not self.db:
            logger.warning("⚠️ Nenhuma conexão ativa com MongoDB. Tentando reconectar...")
            await self.connect()

        if not self.db:
            raise ConnectionError("❌ Erro: Banco de dados não disponível após reconexão!")

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
    """
    Função global para obter o banco de dados.
    """
    return await database.get_database()

async def get_redis():
    """
    Função global para obter o Redis.
    """
    return await database.get_redis()
