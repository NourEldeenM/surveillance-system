import redis
from app.core.config import REDIS

try:
    redis_client = redis.Redis(
        host=REDIS.REDIS_HOST,
        port=REDIS.REDIS_PORT,
        db=REDIS.REDIS_DB,
        decode_responses=True  # Optional: for working with strings directly
    )
    # Test connection (optional)
    redis_client.ping()
except redis.RedisError as e:
    raise ConnectionError(f"Redis connection error: {e}")
