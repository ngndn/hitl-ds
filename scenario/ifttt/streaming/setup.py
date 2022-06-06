import redis

if __name__ == '__main__':
    redis_client = redis.Redis('localhost', 6379)
    redis_client.set('counter_1', 0)
    redis_client.set('counter_2', 0)
