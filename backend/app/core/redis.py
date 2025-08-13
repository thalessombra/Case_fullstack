# app/core/redis.py
import redis.asyncio as aioredis
from typing import Optional
from app.core.config import settings

_redis_client: Optional[aioredis.Redis] = None

def get_redis_client() -> aioredis.Redis:
    """
    Retorna um cliente Redis singleton (async).
    Use get_redis_client() diretamente nos endpoints (await client.get(...)).
    """
    global _redis_client
    if _redis_client is None:
        # settings.REDIS_URL deve existir no seu settings
        _redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client
