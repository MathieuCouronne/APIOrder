from peewee import Model, FloatField, CharField, BooleanField, AutoField
from src.config.database import database


class BaseModel(Model):
    class Meta:
        database = database

class Product(BaseModel):
    name = CharField()
    id = AutoField()
    in_stock = BooleanField()
    description = CharField()
    price = FloatField()
    weight = FloatField()
    image = CharField()
