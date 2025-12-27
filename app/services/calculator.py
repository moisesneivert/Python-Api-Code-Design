def calculate_average(values: list[float]) -> float:
    if not values:
        raise ValueError("List cannot be empty")

    return sum(values) / len(values)
