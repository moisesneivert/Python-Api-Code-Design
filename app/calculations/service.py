from __future__ import annotations

import math
import statistics
from collections.abc import Sequence

from app.domain.strategies import StrategyRegistry


class CalculationService:
    def __init__(self, registry: StrategyRegistry | None = None) -> None:
        self._registry = registry or StrategyRegistry()

    def calculate(self, operation: str, values: Sequence[float]) -> dict:
        strategy = self._registry.get(operation)
        result = strategy.calculate(values)
        return {
            "operation": operation,
            "result": _normalize(result),
            "count": len(values),
        }

    def weighted_mean(
        self,
        values: Sequence[float],
        weights: Sequence[float],
    ) -> dict:
        weighted_sum = math.fsum(
            value * weight for value, weight in zip(values, weights, strict=True)
        )
        result = weighted_sum / math.fsum(weights)
        return {
            "operation": "weighted_mean",
            "result": _normalize(result),
            "count": len(values),
        }

    def statistics_summary(
        self,
        values: Sequence[float],
        *,
        sample: bool = False,
    ) -> dict:
        variance = (
            statistics.variance(values) if sample else statistics.pvariance(values)
        )
        standard_deviation = (
            statistics.stdev(values) if sample else statistics.pstdev(values)
        )
        return {
            "count": len(values),
            "sum": _normalize(math.fsum(values)),
            "minimum": _normalize(min(values)),
            "maximum": _normalize(max(values)),
            "mean": _normalize(math.fsum(values) / len(values)),
            "median": _normalize(float(statistics.median(values))),
            "variance": _normalize(variance),
            "standard_deviation": _normalize(standard_deviation),
            "sample": sample,
        }

    def operation_catalog(self) -> dict:
        built_in = [
            {
                "key": item.key,
                "label": item.label,
                "description": item.description,
                "endpoint": item.endpoint,
            }
            for item in self._registry.catalog()
        ]
        built_in.extend(
            [
                {
                    "key": "weighted_mean",
                    "label": "Weighted mean",
                    "description": "Mean in which each value has an associated weight.",
                    "endpoint": "/api/v1/calculations/weighted-mean",
                },
                {
                    "key": "statistics",
                    "label": "Statistical summary",
                    "description": "Descriptive statistics for a set of numbers.",
                    "endpoint": "/api/v1/calculations/statistics",
                },
            ]
        )
        return {"operations": built_in}


def _normalize(value: float) -> float:
    if value == 0:
        return 0.0
    return float(value)
