def test_root_returns_service_links(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["documentation"] == "/docs"
    assert response.json["openapi"] == "/openapi.json"


def test_health_returns_service_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {
        "status": "ok",
        "service": "Python Calculation API",
        "version": "1.0.0",
    }


def test_response_contains_generated_request_id(client):
    response = client.get("/health")

    assert len(response.headers["X-Request-ID"]) == 32
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Cache-Control"] == "no-store"


def test_response_preserves_supplied_request_id(client):
    response = client.get("/health", headers={"X-Request-ID": "trace-123"})

    assert response.headers["X-Request-ID"] == "trace-123"


def test_unknown_route_uses_problem_format(client):
    response = client.get("/missing")

    assert response.status_code == 404
    assert response.json["error"]["code"] == "not_found"
    assert response.json["error"]["request_id"]


def test_method_not_allowed_uses_problem_format(client):
    response = client.get("/api/v1/calculations/arithmetic-mean")

    assert response.status_code == 405
    assert response.json["error"]["code"] == "method_not_allowed"


def test_openapi_document_is_available(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json["info"]["title"] == "Python Calculation API"
    assert "/api/v1/calculations/statistics" in response.json["paths"]
