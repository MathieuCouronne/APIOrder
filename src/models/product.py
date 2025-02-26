from peewee import Model, FloatField, CharField, BooleanField, IntegerField
from src.config.database import database


class BaseModel(Model):
    class Meta:
        database = database

class Product(BaseModel):
    name = CharField()
    id = IntegerField()
    in_stock = BooleanField()
    description = CharField()
    price = FloatField()
    weight = FloatField()
    image = CharField()
