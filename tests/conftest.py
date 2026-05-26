"""Configuración de pytest: carga .env y omite tests si no hay base de datos."""

import os

import pytest
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("DATABASE_URL"):
    pytest.skip(
        "DATABASE_URL no definida (configura .env o exporta la variable).",
        allow_module_level=True,
    )

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-local-pytest-32chars!!")

_cors = os.getenv("CORS_ORIGINS", "")
for origin in ("http://localhost:4200", "http://127.0.0.1:4200"):
    if origin not in _cors:
        _cors = f"{_cors},{origin}" if _cors else origin
os.environ["CORS_ORIGINS"] = _cors

from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
