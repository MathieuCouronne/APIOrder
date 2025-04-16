import redis
from rq import Worker, Queue, connections
from src.config.database import redis_conn

listen = ['payment_queue']


if __name__ == '__main__':
    queue = Queue('payment_queue', connection=redis_conn)
    worker = Worker([queue])
    worker.work()