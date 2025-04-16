import urllib.request
import ssl
import json
from src.models.product import Product

PRODUCTS_URL = "http://dimensweb.uqac.ca/~jgnault/shops/products/"

def clean_string(s: str) -> str:
    if s:
        return s.replace('\x00', '')
    return s

def fetch_and_store_products():
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(PRODUCTS_URL, context=context) as response:
            data = json.loads(response.read().decode())

            print(data)

            products = data.get("products", [])

            for p in products:
                existing_product = Product.get_or_none(Product.id == p["id"])

                # Nettoyage des chaînes avant de les utiliser
                name = clean_string(p["name"])
                description = clean_string(p["description"])
                image = clean_string(p["image"])

                if existing_product:
                    existing_product.name = name
                    existing_product.description = description
                    existing_product.price = p["price"]
                    existing_product.in_stock = p["in_stock"]
                    existing_product.weight = p["weight"]
                    existing_product.image = image
                    existing_product.save()
                    print(f"Produit mis à jour : {existing_product.name}")
                else:
                    Product.create(
                        id=p["id"],
                        name=name,
                        description=description,
                        price=p["price"],
                        in_stock=p["in_stock"],
                        weight=p["weight"],
                        image=image
                    )
                    print(f"Produit ajouté : {name}")

    except Exception as e:
        print(f"Erreur lors de la récupération des produits : {e}")
