import redis

if __name__ == '__main__':
    redis_client = redis.Redis('localhost', 6379)
    redis_client.set('moved', 0)
