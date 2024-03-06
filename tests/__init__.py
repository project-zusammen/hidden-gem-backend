import redis
import logging as log
from app.test_settings import redis_cache_config

def test_redis_connection():
    try:
        redis_client = redis.StrictRedis(redis_cache_config)
        redis_client.ping()
        log.info("Redis connection is successful.")
    except redis.ConnectionError as e:
        log.info(f"Error connecting to Redis: {e}")

if __name__ == "__main__":
    test_redis_connection()
