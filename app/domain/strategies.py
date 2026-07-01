from __future__ import annotations

import math
import statistics
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass

from app.domain.exceptions import CalculationError


@dataclass(frozen=True, slots=True)
class OperationDescription:
    key: str
    label: str
    description: str
    endpoint: str


class CalculationStrategy(ABC):
    description: OperationDescription

    @abstractmethod
    def calculate(self, values: Sequence[float]) -> float:
        """Calculate and return one numeric result."""


class ArithmeticMeanStrategy(CalculationStrategy):
    description = OperationDescription(
        key="arithmetic_mean",
        label="Arithmetic mean",
        description="Sum of all values divided by the number of values.",
        endpoint="/api/v1/calculations/arithmetic-mean",
    )

    def calculate(self, values: Sequence[float]) -> float:
        _require_values(values)
        return math.fsum(values) / len(values)


class MedianStrategy(CalculationStrategy):
    description = OperationDescription(
        key="median",
        label="Median",
        description="Middle value after sorting the input values.",
        endpoint="/api/v1/calculations/median",
    )

    def calculate(self, values: Sequence[float]) -> float:
        _require_values(values)
        return float(statistics.median(values))


class StrategyRegistry:
    def __init__(self, strategies: Sequence[CalculationStrategy] | None = None) -> None:
        configured = strategies or [ArithmeticMeanStrategy(), MedianStrategy()]
        self._strategies = {
            strategy.description.key: strategy for strategy in configured
        }

    def get(self, operation: str) -> CalculationStrategy:
        try:
            return self._strategies[operation]
        except KeyError as exc:
            raise CalculationError(
                f"Unsupported operation: {operation}.",
                code="unsupported_operation",
                details={"operation": operation},
            ) from exc

    def catalog(self) -> list[OperationDescription]:
        return [strategy.description for strategy in self._strategies.values()]


def _require_values(values: Sequence[float]) -> None:
    if not values:
        raise CalculationError(
            "At least one value is required.",
            code="empty_values",
        )
