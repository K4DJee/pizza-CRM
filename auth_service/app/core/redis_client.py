import redis.asyncio as redis
from config import config

redis_client = redis.Redis.from_url(
    url=config.REDIS_URL,
    decode_responses=True
)