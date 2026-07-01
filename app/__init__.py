from __future__ import annotations

import logging
import os
import uuid
from typing import Any

from dotenv import load_dotenv
from flask import Flask, g, jsonify, request

from app.config import Config
from app.errors import register_error_handlers
from app.extensions import api


def create_app(config: dict[str, Any] | None = None) -> Flask:
    """Create and configure the Flask application."""
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    if config:
        app.config.update(config)

    configure_logging(app)
    register_request_context(app)

    api.init_app(app)
    register_blueprints()
    register_error_handlers(app)
    register_root_route(app)

    return app


def configure_logging(app: Flask) -> None:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    app.logger.setLevel(level)


def register_request_context(app: Flask) -> None:
    @app.before_request
    def assign_request_id() -> None:
        supplied_id = request.headers.get("X-Request-ID", "").strip()
        g.request_id = supplied_id[:128] if supplied_id else uuid.uuid4().hex

    @app.after_request
    def add_response_headers(response):
        response.headers["X-Request-ID"] = g.get("request_id", "")
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        return response


def register_blueprints() -> None:
    from app.calculations.routes import blueprint as calculations_blueprint
    from app.health.routes import blueprint as health_blueprint

    api.register_blueprint(health_blueprint)
    api.register_blueprint(calculations_blueprint)


def register_root_route(app: Flask) -> None:
    @app.get("/")
    def index():
        return jsonify(
            {
                "name": app.config["API_TITLE"],
                "version": app.config["API_VERSION"],
                "documentation": "/docs",
                "openapi": "/openapi.json",
                "health": "/health",
            }
        )
