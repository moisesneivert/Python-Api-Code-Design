class AverageRequestSchema:

    @staticmethod
    def validate(data: dict) -> list[float]:
        if "values" not in data:
            raise ValueError("Field 'values' is required")

        if not isinstance(data["values"], list):
            raise ValueError("'values' must be a list")

        return data["values"]
