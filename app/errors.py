from __future__ import annotations

from typing import Any

from flask import Flask, g, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.domain.exceptions import CalculationError


def _problem(
    *,
    status: int,
    code: str,
    message: str,
    details: Any = None,
):
    payload: dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
            "request_id": g.get("request_id", ""),
        }
    }
    if details:
        payload["error"]["details"] = details
    return jsonify(payload), status


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(CalculationError)
    def handle_calculation_error(exc: CalculationError):
        return _problem(
            status=exc.status_code,
            code=exc.code,
            message=str(exc),
            details=exc.details,
        )

    @app.errorhandler(ValidationError)
    def handle_validation_error(exc: ValidationError):
        return _problem(
            status=422,
            code="validation_error",
            message="The request payload is invalid.",
            details=exc.messages,
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        data = getattr(exc, "data", {}) or {}
        details = data.get("messages") or data.get("errors")
        message = data.get("message") or exc.description
        code = (
            "validation_error"
            if exc.code == 422
            else exc.name.lower().replace(" ", "_")
        )
        return _problem(
            status=exc.code or 500,
            code=code,
            message=message,
            details=details,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc: Exception):
        app.logger.exception("Unexpected error", exc_info=exc)
        return _problem(
            status=500,
            code="internal_server_error",
            message="An unexpected error occurred.",
        )
