def test_calculate_average_success(client):
    response = client.post(
        "/calculator/average",
        json={"values": [1, 2, 3, 4]}
    )

    assert response.status_code == 200
    assert response.json == {"average": 2.5}


def test_calculate_average_invalid_payload(client):
    response = client.post(
        "/calculator/average",
        json={"value": [1, 2, 3]}
    )

    assert response.status_code == 400
