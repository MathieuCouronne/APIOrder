import pytest
from src import create_app
from src.config.database import database
from src.models.order import Order
from src.models.product import Product

@pytest.fixture
def app():
    """Crée une application Flask de test"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DATABASE": "sqlite:///:memory:"  # Utilisation d'une BD temporaire
    })

    with app.app_context():
        database.init(":memory:")  # Utilisation d'une BD en mémoire
        database.create_tables([Product, Order])  # Crée les tables pour les tests

    yield app  # Retourne l'application de test

@pytest.fixture
def client(app):
    """Retourne un client de test Flask"""
    return app.test_client()

@pytest.fixture
def init_db():
    """Ajoute des produits de test dans la base"""
    with database.atomic():
        Product.create(id=1, name="Produit A", price=10.0, in_stock=True)
        Product.create(id=2, name="Produit B", price=20.0, in_stock=True)
