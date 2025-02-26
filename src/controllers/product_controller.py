from src.models.product import Product

def get_all_products():
    return [product_to_dict(p) for p in Product.select()]

def product_to_dict(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "in_stock": product.in_stock,
        "weight": product.weight,
        "image": product.image
    }