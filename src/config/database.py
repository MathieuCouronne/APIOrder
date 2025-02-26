from peewee import SqliteDatabase
import os

DATABASE_PATH = os.getenv('DATABASE','database.db')
database = SqliteDatabase(DATABASE_PATH)

def init_db():
    from src.models.order import Order
    from src.models.product import Product
    database.connect()

    if database.is_closed():
        database.connect()

    if not database.table_exists("product") or not database.table_exists("order"):
        database.create_tables([Product, Order])

    database.close()

