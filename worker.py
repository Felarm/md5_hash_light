import requests, redis
from rq import Worker, Queue, Connection

listen = ['default']
redis_url = 'redis://redis:6379/0'
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
