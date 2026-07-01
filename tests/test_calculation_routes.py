import math


def test_operations_catalog(client):
    response = client.get("/api/v1/calculations/operations")

    assert response.status_code == 200
    assert {item["key"] for item in response.json["operations"]} == {
        "arithmetic_mean",
        "median",
        "weighted_mean",
        "statistics",
    }


def test_arithmetic_mean(client):
    response = client.post(
        "/api/v1/calculations/arithmetic-mean",
        json={"values": [10, 20, 30]},
    )

    assert response.status_code == 200
    assert response.json == {
        "operation": "arithmetic_mean",
        "result": 20.0,
        "count": 3,
    }


def test_arithmetic_mean_handles_decimal_and_negative_values(client):
    response = client.post(
        "/api/v1/calculations/arithmetic-mean",
        json={"values": [-2.5, 0, 5.5]},
    )

    assert response.status_code == 200
    assert response.json["result"] == 1.0


def test_median_with_odd_number_of_values(client):
    response = client.post(
        "/api/v1/calculations/median",
        json={"values": [9, 1, 5]},
    )

    assert response.status_code == 200
    assert response.json["result"] == 5.0


def test_median_with_even_number_of_values(client):
    response = client.post(
        "/api/v1/calculations/median",
        json={"values": [1, 2, 8, 10]},
    )

    assert response.status_code == 200
    assert response.json["result"] == 5.0


def test_weighted_mean(client):
    response = client.post(
        "/api/v1/calculations/weighted-mean",
        json={"values": [7, 8, 10], "weights": [2, 3, 5]},
    )

    assert response.status_code == 200
    assert response.json == {
        "operation": "weighted_mean",
        "result": 8.8,
        "count": 3,
    }


def test_population_statistics(client):
    response = client.post(
        "/api/v1/calculations/statistics",
        json={"values": [2, 4, 4, 4, 5, 5, 7, 9]},
    )

    assert response.status_code == 200
    assert response.json["count"] == 8
    assert response.json["sum"] == 40.0
    assert response.json["mean"] == 5.0
    assert response.json["median"] == 4.5
    assert response.json["variance"] == 4.0
    assert response.json["standard_deviation"] == 2.0
    assert response.json["sample"] is False


def test_sample_statistics(client):
    response = client.post(
        "/api/v1/calculations/statistics",
        json={"values": [1, 2, 3], "sample": True},
    )

    assert response.status_code == 200
    assert response.json["variance"] == 1.0
    assert response.json["standard_deviation"] == 1.0
    assert response.json["sample"] is True


def test_stable_sum_for_floating_point_values(client):
    response = client.post(
        "/api/v1/calculations/arithmetic-mean",
        json={"values": [1e16, 1, -1e16]},
    )

    assert response.status_code == 200
    assert math.isclose(response.json["result"], 1 / 3)
