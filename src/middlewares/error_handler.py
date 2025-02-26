from flask import jsonify

class APIError(Exception):
    def __init__(self, code, message, status_code=422):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {
            "errors": {
                "product": {
                    "code": self.code,
                    "name": self.message
                }
            }
        }

def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Ressource introuvable"}), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({"error": "Données invalides"}), 422
