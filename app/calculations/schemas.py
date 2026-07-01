from __future__ import annotations

import math

from marshmallow import (
    RAISE,
    Schema,
    ValidationError,
    fields,
    validate,
    validates_schema,
)

MAX_VALUES = 1_000


def finite_number(value: float) -> None:
    if not math.isfinite(value):
        raise ValidationError("Value must be a finite number.")


number_field = fields.Float(
    required=True,
    allow_nan=True,
    validate=finite_number,
    metadata={"example": 10.5},
)


class StrictSchema(Schema):
    class Meta:
        unknown = RAISE


class ValuesRequestSchema(StrictSchema):
    values = fields.List(
        number_field,
        required=True,
        validate=validate.Length(min=1, max=MAX_VALUES),
        metadata={"example": [10, 20, 30]},
    )


class WeightedMeanRequestSchema(ValuesRequestSchema):
    weights = fields.List(
        fields.Float(required=True, allow_nan=True, validate=finite_number),
        required=True,
        validate=validate.Length(min=1, max=MAX_VALUES),
        metadata={"example": [1, 2, 3]},
    )

    @validates_schema
    def validate_weights(self, data, **kwargs) -> None:
        values = data.get("values", [])
        weights = data.get("weights", [])

        if len(values) != len(weights):
            raise ValidationError(
                "Values and weights must have the same length.",
                field_name="weights",
            )
        if any(weight < 0 for weight in weights):
            raise ValidationError(
                "Weights cannot be negative.",
                field_name="weights",
            )
        if math.fsum(weights) <= 0:
            raise ValidationError(
                "The sum of weights must be greater than zero.",
                field_name="weights",
            )


class StatisticsRequestSchema(ValuesRequestSchema):
    sample = fields.Boolean(
        load_default=False,
        metadata={
            "description": "Use sample variance and standard deviation (n - 1).",
            "example": False,
        },
    )

    @validates_schema
    def validate_sample_size(self, data, **kwargs) -> None:
        if data.get("sample") and len(data.get("values", [])) < 2:
            raise ValidationError(
                "Sample statistics require at least two values.",
                field_name="values",
            )


class CalculationResponseSchema(StrictSchema):
    operation = fields.String(required=True)
    result = fields.Float(required=True)
    count = fields.Integer(required=True)


class StatisticsResponseSchema(StrictSchema):
    count = fields.Integer(required=True)
    sum = fields.Float(required=True)
    minimum = fields.Float(required=True)
    maximum = fields.Float(required=True)
    mean = fields.Float(required=True)
    median = fields.Float(required=True)
    variance = fields.Float(required=True)
    standard_deviation = fields.Float(required=True)
    sample = fields.Boolean(required=True)


class OperationSchema(StrictSchema):
    key = fields.String(required=True)
    label = fields.String(required=True)
    description = fields.String(required=True)
    endpoint = fields.String(required=True)


class OperationCatalogSchema(StrictSchema):
    operations = fields.List(fields.Nested(OperationSchema), required=True)


class HealthSchema(StrictSchema):
    status = fields.String(required=True)
    service = fields.String(required=True)
    version = fields.String(required=True)


class ErrorItemSchema(StrictSchema):
    code = fields.String(required=True)
    message = fields.String(required=True)
    request_id = fields.String(required=True)
    details = fields.Raw(required=False, allow_none=True)


class ErrorResponseSchema(StrictSchema):
    error = fields.Nested(ErrorItemSchema, required=True)
