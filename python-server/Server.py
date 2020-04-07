#!/usr/bin/env python3

# step 1: import the redis-py client package
import redis

# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "redis"
redis_port = 6379
redis_password = ""


def hello_redis():
    """Example Hello Redis Program"""
   
    # step 3: create the Redis Connection object
    try:
   
        # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
        # using the default encoding utf-8.  This is client specific.
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
   
       keys = redis.keys('*')
for key in keys:
    type = redis.type(key)
    if type == "string":
        val = redis.get(key)
    if type == "hash":
        vals = redis.hgetall(key)
    if type == "zset":
        vals = redis.zrange(key, 0, -1)
    if type == "list":
        vals = redis.lrange(key, 0, -1)
    if type == "set":
        vals = redis. smembers(key)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    hello_redis()
