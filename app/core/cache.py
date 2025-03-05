# app/core/cache.py

import redis.asyncio as redis
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do Redis
REDIS_URI = os.getenv("REDIS_URI", "redis://maglev.proxy.rlwy.net:17929")

# Inicializa a conexão com o Redis
class RedisCache:
    def __init__(self):
        self.redis = None

    async def connect(self):
        """
        Conecta ao Redis.
        """
        if not self.redis:
            self.redis = redis.Redis.from_url(REDIS_URI, decode_responses=True)

    async def set_cache(self, key: str, value: str, ttl: int = 300):
        """
        Define um valor no cache com tempo de expiração.
        """
        await self.redis.setex(key, ttl, value)

    async def get_cache(self, key: str):
        """
        Obtém um valor do cache.
        """
        return await self.redis.get(key)

    async def clear_cache(self, key: str):
        """
        Remove um valor do cache.
        """
        await self.redis.delete(key)

# Instância global do cache
cache = RedisCache()

async def get_redis_cache():
    await cache.connect()
    return cache
