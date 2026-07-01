import math

import pytest

from app.calculations.service import CalculationService
from app.domain.exceptions import CalculationError
from app.domain.strategies import (
    ArithmeticMeanStrategy,
    MedianStrategy,
    StrategyRegistry,
)


def test_arithmetic_strategy_rejects_empty_sequence():
    with pytest.raises(CalculationError, match="At least one value"):
        ArithmeticMeanStrategy().calculate([])


def test_median_strategy_rejects_empty_sequence():
    with pytest.raises(CalculationError, match="At least one value"):
        MedianStrategy().calculate([])


def test_registry_rejects_unknown_operation():
    registry = StrategyRegistry()

    with pytest.raises(CalculationError) as exc_info:
        registry.get("mode")

    assert exc_info.value.code == "unsupported_operation"
    assert exc_info.value.details == {"operation": "mode"}


def test_registry_can_receive_custom_strategy_collection():
    registry = StrategyRegistry([MedianStrategy()])

    assert registry.get("median").calculate([1, 3, 2]) == 2.0
    assert [item.key for item in registry.catalog()] == ["median"]


def test_service_normalizes_negative_zero():
    result = CalculationService().calculate("arithmetic_mean", [-0.0, 0.0])

    assert result["result"] == 0.0
    assert math.copysign(1, result["result"]) == 1.0


def test_operation_catalog_contains_endpoint_metadata():
    catalog = CalculationService().operation_catalog()

    arithmetic = next(
        item for item in catalog["operations"] if item["key"] == "arithmetic_mean"
    )
    assert arithmetic["endpoint"].endswith("/arithmetic-mean")
