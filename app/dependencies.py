from config import redis_host, redis_port, redis_db
import redis

def get_redis_instance():
    return redis.StrictRedis(host=redis_host, port=int(redis_port), db=int(redis_db))
