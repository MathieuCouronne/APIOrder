from peewee import Model, AutoField, BooleanField, ForeignKeyField, FloatField, CharField, TextField, IntegerField
from src.config.database import database
from src.models.product import Product
import json

class BaseModel(Model):
    class Meta:
        database = database

class Order(BaseModel):
    id = AutoField()
    product = ForeignKeyField(Product, backref="orders")
    quantity = IntegerField()
    total_price_tax = FloatField(null=True, default=None)
    total_price = FloatField(null=True, default=None)
    shipping_price = FloatField(null=True, default=None)
    email = CharField(null=True, default=None)
    paid = BooleanField(default=False)

    shipping_information = TextField(null=True)
    transaction = TextField(null=True)
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

    def get_transaction(self):
        try:
            return json.loads(self.transaction) if self.transaction else {}
        except json.JSONDecodeError:
            return {}
