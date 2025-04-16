from flask import Blueprint, request, jsonify
from src.controllers.order_controller import create_order, get_order, update_order, process_payement
from src.controllers.product_controller import get_all_products
from src.middlewares.error_handler import APIError
from flask import render_template
from src.config.database import queue



api = Blueprint("api", __name__)

@api.route("/")
def home():
    return render_template("create_order.html")

@api.route("/", methods=["GET"])
def get_products():
    return {"products": get_all_products()}


@api.route("/order", methods=["POST"])
def post_order():
    # Récupérer les données envoyées via le formulaire HTML classique
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')

    # Validation des données
    if not product_id or not quantity:
        raise APIError("missing-fields", "La création d'une commande nécessite un produit et une quantité")

    try:
        product_id = int(product_id)
        quantity = int(quantity)
    except ValueError:
        raise APIError("invalid-data", "Les ID de produit et la quantité doivent être des nombres valides")

    return create_order(product_id, quantity)

@api.route("/order/<int:order_id>", methods=["GET"])
def get_order_by_id(order_id):
    response = get_order(order_id)
    return response

@api.route("/order/<int:order_id>", methods=["PUT"])
def put_order(order_id):
    data = request.get_json()

    if "credit_card" in data and ("shipping_information" in data or "email" in data):
        return jsonify({
            "errors": {
                "order": {
                    "code": "invalid-request",
                    "message": "On ne peut pas fournir credit_card avec shipping_information et/ou email",
                }
            }
        }), 422
    if "credit_card" in data:
        job = queue.enqueue(process_payement, order_id, data["credit_card"])
        return jsonify({"job_id": job.get_id(), "status": "queued"}), 202
    return update_order(order_id, data)
