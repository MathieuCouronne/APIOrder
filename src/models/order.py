from peewee import Model, IntegerField, BooleanField, ForeignKeyField, FloatField, CharField, TextField
from src.config.database import database
from src.models.product import Product
import json

class BaseModel(Model):
    class Meta:
        database = database

class Order(BaseModel):
    id = IntegerField(primary_key=True)
    product = ForeignKeyField(Product, backref="orders")
    quantity = IntegerField()
    total_price_tax = FloatField(null=True, default=None)
    total_price = FloatField(null=True, default=None)
    shipping_price = FloatField(null=True, default=None)
    email = CharField(null=True, default=None)
    paid = BooleanField(default=False)

    shipping_information = TextField(null=True)
    credit_card = TextField(null=True)

    def get_shipping_information(self):
        try:
            return json.loads(self.shipping_information) if self.shipping_information else {}
        except json.JSONDecodeError:
            return {}

    def get_credit_card(self):
        try:
            return json.loads(self.credit_card) if self.credit_card else {}
        except json.JSONDecodeError:
            return {}