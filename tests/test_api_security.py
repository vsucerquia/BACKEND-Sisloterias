from fastapi.testclient import TestClient


def test_cors_preflight_allows_localhost_4200(client: TestClient) -> None:
    response = client.options(
        "/jugadores/",
        headers={
            "Origin": "http://localhost:4200",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Authorization, Content-Type",
        },
    )

    assert response.status_code in (200, 204)
    assert response.headers.get("access-control-allow-origin") == "http://localhost:4200"
    allow_headers = response.headers.get("access-control-allow-headers", "").lower()
    assert "authorization" in allow_headers


def test_protected_endpoint_requires_bearer_token(client: TestClient) -> None:
    response = client.get("/jugadores/")

    assert response.status_code == 401
    body = response.json()
    assert "detail" in body


def test_protected_endpoint_rejects_invalid_token(client: TestClient) -> None:
    response = client.get(
        "/jugadores/",
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False
    assert body["error"]
