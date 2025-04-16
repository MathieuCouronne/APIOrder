from peewee import PostgresqlDatabase
from rq import Queue
from redis import Redis
import redis
import os

database = PostgresqlDatabase(
    os.getenv("DB_NAME", "api8inf349"),
    user=os.getenv("DB_USER", "user1"),
    password=os.getenv("DB_PASSWORD", "pass"),
    host=os.getenv("DB_HOST", "db"),
    port=int(os.getenv("DB_PORT", "5432"))
)
redis_conn = Redis(host='host.docker.internal', port=6379, db=0)
queue = Queue('payment_queue', connection=redis_conn)
redis_client = redis.StrictRedis.from_url(os.getenv("REDIS_URL", "redis://host.docker.internal:6379"), decode_responses=True)

def init_db():
    from src.models.order import Order
    from src.models.product import Product
    database.connect()

    if database.is_closed():
        database.connect()

    if not database.table_exists("product") or not database.table_exists("order"):
        print("Creating database")
        database.create_tables([Product, Order])

    database.close()

