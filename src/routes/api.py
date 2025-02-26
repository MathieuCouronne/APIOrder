from idlelib.iomenu import errors

from flask import Blueprint, request, jsonify
from src.controllers.order_controller import create_order, get_order, update_order, process_payement
from src.controllers.product_controller import get_all_products


api = Blueprint("api", __name__)

@api.route("/", methods=["GET"])
def get_products():
    return {"products": get_all_products()}


@api.route("/order", methods=["POST"])
def post_order():
    data = request.get_json()
    return create_order(data)

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
        return process_payement(order_id, data["credit_card"])
    return update_order(order_id, data)
