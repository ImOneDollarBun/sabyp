import redis
from config import Redis

r = redis.Redis(host=Redis.HOST, port=Redis.PORT, decode_responses=True)