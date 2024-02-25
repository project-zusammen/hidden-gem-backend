import redis
from app.test_settings import redis_cache_config

def test_redis_connection():
    try:
        redis_client = redis.StrictRedis(redis_cache_config)
        redis_client.ping()
        print("Redis connection is successful.")
    except redis.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")

if __name__ == "__main__":
    test_redis_connection()
