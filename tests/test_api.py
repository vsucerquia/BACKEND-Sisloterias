import os

from fastapi.testclient import TestClient

SEED_USER = os.getenv("SEED_ADMIN_USER", "admin")
SEED_PASSWORD = os.getenv("SEED_ADMIN_PASSWORD", "admin123")


def test_root_public(client: TestClient) -> None:
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()


def test_jugadores_sin_token_401(client: TestClient) -> None:
    r = client.get("/jugadores/")
    assert r.status_code == 401


def test_login_ok(client: TestClient) -> None:
    r = client.post(
        "/auth/login",
        data={"username": SEED_USER, "password": SEED_PASSWORD},
    )
    assert r.status_code == 200
    body = r.json()
    assert body.get("token_type") == "bearer"
    assert "access_token" in body


def test_jugadores_con_token(client: TestClient) -> None:
    login = client.post(
        "/auth/login",
        data={"username": SEED_USER, "password": SEED_PASSWORD},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    r = client.get("/jugadores/", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
