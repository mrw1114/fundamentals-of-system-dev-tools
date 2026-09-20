import redis, os, time
r = redis.Redis(host='redis', port=6379)
while True:
    r.incr('counter')
    print('Counter:', r.get('counter'))
    time.sleep(2)
