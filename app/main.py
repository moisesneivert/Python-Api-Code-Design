from flask import Flask
from flasgger import Swagger
from app.routes.calculator import calculator_bp

def create_app(testing: bool = False):
    app = Flask(__name__)

    app.config["SWAGGER"] = {
        "title": "Python API - Code Design",
        "uiversion": 3
    }

    Swagger(app)

    if testing:
        app.config["TESTING"] = True

    app.register_blueprint(calculator_bp)
    return app
