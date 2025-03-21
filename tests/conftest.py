import pytest
from src import create_app
from src.config import database
from src.config.database import init_db, database
from src.models.product import Product
from src.models.order import Order
from src.services.product_service import fetch_and_store_products


@pytest.fixture
def app():
    app = create_app()
    app.config['DATABASE'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        init_db()
        fetch_and_store_products()

    yield app

    with database.connection_context():
        database.drop_tables([Product, Order])

@pytest.fixture
def client(app):
    return app.test_client()