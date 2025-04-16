from flask import jsonify
import urllib.request
import ssl
from src.models.order import Order
from src.models.product import Product
from src.middlewares.error_handler import APIError
import json

from src.services.order_service import get_cached_order, cache_order


def get_tax_rate(province):
    tax_rates = {
        "QC": 0.15,
        "ON": 0.13,
        "AB": 0.05,
        "BC": 0.12,
        "NS": 0.14
    }
    return tax_rates.get(province, 0)

def calculate_shipping_price(total_weight):
    if total_weight < 500:
        return 5
    elif total_weight < 2000:
        return 10
    else:
        return 25



def create_order(data):
    if "product" not in data or "id" not in data["product"] or "quantity" not in data["product"]:
        raise APIError("missing-fields", "La création d'une commande nécessite un produit")

    product_id = data["product"]["id"]
    quantity = data["product"]["quantity"]

    if quantity < 1:
        raise APIError("invalid-quantity", "La quantité doit être au moins de 1")

    product = Product.get_or_none(Product.id == product_id)
    if product is None:
        raise APIError("invalid-product", "Le produit n'existe pas")

    if not product.in_stock:
        raise APIError("out-of-inventory", "Le produit demandé n'est pas en inventaire")

    order = Order.create(product=product, quantity=quantity)
    return "", 302, {"Location": f"/order/{order.id}"}

# Function to get an order
# Call with a Get request and an id as param

def get_order(order_id):

    cached_order = get_cached_order(order_id)
    if cached_order:
        return cached_order

    order = Order.get_or_none(Order.id == order_id)
    if order is None:
        raise APIError("not-found", "Commande introuvable", status_code=404)

    order.total_price = order.quantity * order.product.price

    total_weight = order.quantity * order.product.weight
    order.shipping_price = calculate_shipping_price(total_weight)


    response_data = {
        "order": {
            "id": order.id,
            "total_price": order.total_price,
            "total_price_tax": order.total_price_tax,
            "email": order.email,
            "credit_card": order.get_credit_card(),
            "shipping_information": order.get_shipping_information(),
            "paid": order.paid,
            "transaction": order.get_transaction(),
            "product": {
                "id": order.product.id,
                "quantity": order.quantity
            },
            "shipping_price": order.shipping_price,
        }
    }
    order.save()
    if order.paid:
        cache_order(order_id, response_data)
    return jsonify(response_data)

# Function to update the order with shipping info and mail
# Call by a PUT request take an id as param

def update_order(order_id, data):
    order = Order.get_or_none(Order.id == order_id)
    if order is None:
        raise APIError("not-found", "Commande introuvable", status_code=404)

    if "order" not in data:
        raise APIError("missing-fields", "Il manque l'objet 'order' dans la requête", status_code=422)

    order_data = data["order"]
    required_fields = ["email", "shipping_information"]
    required_shipping_fields = ["country", "address", "postal_code", "city", "province"]

    #Checking each fields to know if one of some are missing

    for field in required_fields:
        if field not in order_data:
            raise APIError("missing-fields", f"Le champ '{field}' est obligatoire", status_code=422)

    shipping_info = order_data["shipping_information"]
    for field in required_shipping_fields:
        if field not in shipping_info:
            raise APIError("missing-fields", f"Le champ 'shipping_information.{field}' est obligatoire", status_code=422)

    #calcul total price with tax rate
    tax_rate = get_tax_rate(shipping_info["province"])
    if order.total_price is None:
        order.total_price = order.quantity * order.product.price
    order.total_price_tax = round(order.total_price * (1 + tax_rate), 2)
    order.email = order_data["email"]
    order.shipping_information = json.dumps(order_data["shipping_information"])

    order.save()
    return jsonify({
        "order": {
            "id": order.id,
            "shipping_information": json.loads(order.shipping_information),
            "credit_card": json.loads(order.credit_card) if order.credit_card else {},
            "email": order.email,
            "total_price": order.quantity * order.product.price,
            "total_price_tax": order.total_price_tax,
            "transaction": {},
            "paid": order.paid,
            "product": {
                "id": order.product.id,
                "quantity": order.quantity
            },
            "shipping_price": order.shipping_price
        }
    }), 200


# Function to create a payment
# Call by a PUT and take an id as param

def process_payement(order_id, data):
    order = Order.get_or_none(Order.id == order_id)
    if order is None:
        raise APIError("not-found", "Commande introuvable", status_code=404)

    if not order.email or not order.shipping_information:
        raise APIError("missing-fields", "Les informations du clinet sont nécessaire avant d'appliquer une carte de crédit", status_code=422)

    if order.paid:
        raise APIError("already_paid", "La commande a déjà été payée", status_code=422)


    if order.total_price_tax is None:
        order.total_price_tax = (order.quantity * order.product.price) * get_tax_rate(
            order.shipping_information["province"])

    if order.shipping_price is None:
        total_weight = order.quantity * order.product.weight
        order.shipping_price = calculate_shipping_price(total_weight)
    payment_data = json.dumps({
        "credit_card": data,
        "amount_charged": order.total_price_tax + order.shipping_price,
    }).encode("utf-8")

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request("https://dimensweb.uqac.ca/~jgnault/shops/pay/", data=payment_data, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, context=context) as response:
            payment_response = json.loads(response.read().decode())
        if response.getcode() != 200:
            return jsonify({
                "errors": {
                    "payment": {
                        "code": "payment-error",
                        "name": "Erreur lors du paiement, code HTTP inattendu."
                    }
                }
            }), response.getcode()
        order.paid = True
        order.credit_card = json.dumps({
            "name": data["name"],
            "first_digits": data["number"][:4],
            "last_digits": data["number"][-4:],
            "expiration_year": data["expiration_year"],
            "expiration_month": data["expiration_month"]
        })

        order.transaction = json.dumps(payment_response["transaction"])
        order.save()
        response_data =  {
            "order": {
                "id": order.id,
                "shipping_information": json.loads(order.shipping_information),
                "email": order.email,
                "total_price": order.quantity * order.product.price,
                "total_price_tax": order.total_price_tax,
                "paid": order.paid,
                "product": {
                    "id": order.product.id,
                    "quantity": order.quantity
                },
                "credit_card": json.loads(order.credit_card),
                "transaction": json.loads(order.transaction),
                "shipping_price": order.shipping_price
            }
        }
        cache_order(order_id, response_data)
        return response_data

    except urllib.error.HTTPError as e:
        return jsonify({
            "errors": {
                "payment": {
                    "code": "payment-error",
                    "name": f"Erreur lors du paiement : {e}"
                }
            }
        }), e.code

    except urllib.error.URLError as e:
        return jsonify({
            "errors": {
                "payment": {
                    "code": "service-unavailable",
                    "name": "Le service de paiement est actuellement indisponible."
                }
            }
        }), 503