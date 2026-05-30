import os

from fastapi.testclient import TestClient

SEED_USER = os.getenv("SEED_ADMIN_USER", "admin")
SEED_PASSWORD = os.getenv("SEED_ADMIN_PASSWORD", "admin123")

PROTECTED_LIST_ROUTES = (
    "/jugadores/",
    "/juegos/",
    "/sorteos/",
    "/boletos/",
    "/premios/",
    "/pagos/",
)


def _login(client: TestClient) -> str:
    response = client.post(
        "/auth/login",
        data={"username": SEED_USER, "password": SEED_PASSWORD},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_root_public(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_login_ok(client: TestClient) -> None:
    response = client.post(
        "/auth/login",
        data={"username": SEED_USER, "password": SEED_PASSWORD},
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("token_type") == "bearer"
    assert "access_token" in body


def test_login_bad_credentials(client: TestClient) -> None:
    response = client.post(
        "/auth/login",
        data={"username": SEED_USER, "password": "clave-incorrecta"},
    )
    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False
    assert body["error"]


def test_protected_routes_require_auth(client: TestClient) -> None:
    for route in PROTECTED_LIST_ROUTES:
        response = client.get(route)
        assert response.status_code == 401, route


def test_protected_routes_list_with_token(client: TestClient) -> None:
    token = _login(client)
    headers = {"Authorization": f"Bearer {token}"}

    for route in PROTECTED_LIST_ROUTES:
        response = client.get(route, headers=headers)
        assert response.status_code == 200, route
        assert isinstance(response.json(), list)
