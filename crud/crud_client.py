"""Cliente HTTP genérico para operaciones CRUD contra la API REST."""

from __future__ import annotations

import os

import requests


class CrudClient:
    """Envía GET/POST/PUT/DELETE a ``base_url``; opcional Bearer desde ``API_BEARER_TOKEN``."""

    def __init__(self, base_url: str | None = None) -> None:
        env_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
        self.base_url = (base_url or env_url).rstrip("/")

    def _headers(self) -> dict:
        token = os.getenv("API_BEARER_TOKEN", "").strip()
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

    def _request(self, method, endpoint: str, data: dict | None = None):
        """Ejecuta una petición y devuelve JSON o un dict con error estructurado."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._headers()
        response = None
        try:
            if data is not None:
                response = method(url, json=data, headers=headers)
            else:
                response = method(url, headers=headers)
            response.raise_for_status()

            if response.text:
                return response.json()
            return {"message": "Operación realizada correctamente"}

        except requests.exceptions.HTTPError:
            if response is None:
                return {"success": False, "error": "Error HTTP sin respuesta"}
            try:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.json(),
                }
            except Exception:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text,
                }

        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "status_code": 500,
                "error": "No fue posible conectarse a la API",
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "status_code": 500,
                "error": "La solicitud tardó demasiado tiempo",
            }

        except requests.exceptions.RequestException as exc:
            return {
                "success": False,
                "status_code": 500,
                "error": f"Error inesperado: {str(exc)}",
            }

    def list_all(self, resource: str):
        """GET ``resource/`` — lista todos los registros."""
        return self._request(requests.get, f"{resource}/")

    def get_by_id(self, resource: str, item_id: int):
        """GET ``resource/{id}``."""
        return self._request(requests.get, f"{resource}/{item_id}")

    def create(self, resource: str, data: dict):
        """POST ``resource/`` con cuerpo JSON."""
        return self._request(requests.post, f"{resource}/", data)

    def update(self, resource: str, item_id: int, data: dict):
        """PUT ``resource/{id}`` con cuerpo JSON."""
        return self._request(requests.put, f"{resource}/{item_id}", data)

    def delete(self, resource: str, item_id: int):
        """DELETE ``resource/{id}``."""
        return self._request(requests.delete, f"{resource}/{item_id}")
