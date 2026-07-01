from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint

from app.calculations.schemas import HealthSchema

blueprint = Blueprint(
    "health",
    __name__,
    description="Service health checks.",
)


@blueprint.route("/health")
class HealthResource(MethodView):
    @blueprint.response(200, HealthSchema)
    def get(self):
        """Return the liveness status of the service."""
        return {
            "status": "ok",
            "service": current_app.config["API_TITLE"],
            "version": current_app.config["API_VERSION"],
        }
