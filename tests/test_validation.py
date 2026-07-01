import math

import pytest


@pytest.mark.parametrize(
    ("path", "payload"),
    [
        ("/api/v1/calculations/arithmetic-mean", {"values": []}),
        ("/api/v1/calculations/median", {}),
        ("/api/v1/calculations/statistics", {"values": [1], "sample": True}),
    ],
)
def test_invalid_values_return_422(client, path, payload):
    response = client.post(path, json=payload)

    assert response.status_code == 422
    assert response.json["error"]["code"] == "validation_error"
    assert response.json["error"]["details"]


def test_unknown_field_is_rejected(client):
    response = client.post(
        "/api/v1/calculations/arithmetic-mean",
        json={"values": [1, 2], "unexpected": True},
    )

    assert response.status_code == 422
    assert "unexpected" in str(response.json["error"]["details"])


def test_more_than_one_thousand_values_is_rejected(client):
    response = client.post(
        "/api/v1/calculations/arithmetic-mean",
        json={"values": list(range(1001))},
    )

    assert response.status_code == 422


@pytest.mark.parametrize("invalid", [math.inf, -math.inf, math.nan])
def test_non_finite_values_are_rejected(client, invalid):
    response = client.post(
        "/api/v1/calculations/arithmetic-mean",
        json={"values": [invalid]},
    )

    assert response.status_code == 422
    assert "finite" in str(response.json["error"]["details"]).lower()


def test_weights_must_match_values(client):
    response = client.post(
        "/api/v1/calculations/weighted-mean",
        json={"values": [1, 2], "weights": [1]},
    )

    assert response.status_code == 422
    assert "same length" in str(response.json["error"]["details"])


def test_weights_cannot_be_negative(client):
    response = client.post(
        "/api/v1/calculations/weighted-mean",
        json={"values": [1, 2], "weights": [1, -1]},
    )

    assert response.status_code == 422
    assert "negative" in str(response.json["error"]["details"])


def test_weight_sum_must_be_positive(client):
    response = client.post(
        "/api/v1/calculations/weighted-mean",
        json={"values": [1, 2], "weights": [0, 0]},
    )

    assert response.status_code == 422
    assert "greater than zero" in str(response.json["error"]["details"])


def test_invalid_json_content_type_returns_422(client):
    response = client.post(
        "/api/v1/calculations/arithmetic-mean",
        data="not-json",
        content_type="application/json",
    )

    assert response.status_code in {400, 422}
    assert "error" in response.json
