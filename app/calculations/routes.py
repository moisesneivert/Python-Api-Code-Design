from flask.views import MethodView
from flask_smorest import Blueprint

from app.calculations.schemas import (
    CalculationResponseSchema,
    ErrorResponseSchema,
    OperationCatalogSchema,
    StatisticsRequestSchema,
    StatisticsResponseSchema,
    ValuesRequestSchema,
    WeightedMeanRequestSchema,
)
from app.calculations.service import CalculationService

blueprint = Blueprint(
    "calculations",
    __name__,
    url_prefix="/api/v1/calculations",
    description="Validated mathematical and statistical calculations.",
)
service = CalculationService()


@blueprint.route("/operations")
class OperationCatalogResource(MethodView):
    @blueprint.response(200, OperationCatalogSchema)
    def get(self):
        """List the calculation operations exposed by the API."""
        return service.operation_catalog()


@blueprint.route("/arithmetic-mean")
class ArithmeticMeanResource(MethodView):
    @blueprint.arguments(ValuesRequestSchema)
    @blueprint.response(200, CalculationResponseSchema)
    @blueprint.alt_response(422, schema=ErrorResponseSchema)
    def post(self, payload):
        """Calculate the arithmetic mean of one or more finite numbers."""
        return service.calculate("arithmetic_mean", payload["values"])


@blueprint.route("/median")
class MedianResource(MethodView):
    @blueprint.arguments(ValuesRequestSchema)
    @blueprint.response(200, CalculationResponseSchema)
    @blueprint.alt_response(422, schema=ErrorResponseSchema)
    def post(self, payload):
        """Calculate the median of one or more finite numbers."""
        return service.calculate("median", payload["values"])


@blueprint.route("/weighted-mean")
class WeightedMeanResource(MethodView):
    @blueprint.arguments(WeightedMeanRequestSchema)
    @blueprint.response(200, CalculationResponseSchema)
    @blueprint.alt_response(422, schema=ErrorResponseSchema)
    def post(self, payload):
        """Calculate a weighted mean."""
        return service.weighted_mean(payload["values"], payload["weights"])


@blueprint.route("/statistics")
class StatisticsResource(MethodView):
    @blueprint.arguments(StatisticsRequestSchema)
    @blueprint.response(200, StatisticsResponseSchema)
    @blueprint.alt_response(422, schema=ErrorResponseSchema)
    def post(self, payload):
        """Calculate a descriptive statistical summary."""
        return service.statistics_summary(
            payload["values"],
            sample=payload["sample"],
        )
