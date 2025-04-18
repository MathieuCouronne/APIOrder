import os
from flask import Flask
from src.config.database import init_db
from src.middlewares.error_handler import register_error_handlers
from src.services.product_service import fetch_and_store_products
from src.routes.api import api
from flask_config import Config, TestConfig


def create_app():
    app = Flask(__name__, template_folder="templates")


    env = os.getenv("FLASK_ENV", "development")
    if env == "testing":
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    register_error_handlers(app)


    app.register_blueprint(api)


    return app