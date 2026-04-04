"""Arranca el servidor ASGI (Uvicorn) con la aplicación FastAPI.

Uso:
    python main.py

El servidor queda en http://127.0.0.1:8000 (documentación en /docs).

Para el menú por consola que consume la API vía HTTP, usa en otra terminal::

    python menu_cli.py
"""

import uvicorn


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
