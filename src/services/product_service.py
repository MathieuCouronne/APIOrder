import urllib.request
import json
from src.models.product import Product

PRODUCTS_URL = "http://dimensweb.uqac.ca/~jgnault/shops/products/"

def fetch_and_store_products():
    try:
        with urllib.request.urlopen(PRODUCTS_URL) as response:
            data = json.loads(response.read().decode())

            products = data.get("products", [])

            for p in products:
                existing_product = Product.get_or_none(Product.id == p["id"])

                if existing_product:
                    existing_product.name = p["name"]
                    existing_product.description = p["description"]
                    existing_product.price = p["price"]
                    existing_product.in_stock = p["in_stock"]
                    existing_product.weight = p["weight"]
                    existing_product.image = p["image"]
                    existing_product.save()
                    print(f"Produit mis à jour : {existing_product.name}")
                else:
                    Product.create(
                        id=p["id"],
                        name=p["name"],
                        description=p["description"],
                        price=p["price"],
                        in_stock=p["in_stock"],
                        weight=p["weight"],
                        image=p["image"]
                    )
                    print(f"Produit ajouté : {p['name']}")

    except Exception as e:
        print(f"Erreur lors de la récupération des produits : {e}")
