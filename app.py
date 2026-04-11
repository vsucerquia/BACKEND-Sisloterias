"""Aplicación FastAPI: CORS, manejo centralizado de errores y routers.

Las variables de entorno se cargan en ``database.database`` (``load_dotenv``)
al importar los routers; no hace falta duplicar aquí.
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

from core.error_handlers import app_exception_handler, integrity_exception_handler
from core.exceptions import AppException
from endpoints import (
    auth_router,
    boletos_router,
    juegos_router,
    jugadores_router,
    pagos_router,
    premios_router,
    sorteos_router,
)

_origins_raw = os.getenv(
    "CORS_ORIGINS",
    "http://127.0.0.1:5500,http://localhost:3000,http://127.0.0.1:8000",
)
CORS_ORIGINS = [o.strip() for o in _origins_raw.split(",") if o.strip()]

app = FastAPI(
    title="API Sistema de Lotería",
    version="2.0.0",
    description="Incluye JWT (excepto /auth/login), CORS configurable y errores vía capa core.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)

app.include_router(auth_router.router)
app.include_router(jugadores_router.router)
app.include_router(juegos_router.router)
app.include_router(sorteos_router.router)
app.include_router(boletos_router.router)
app.include_router(premios_router.router)
app.include_router(pagos_router.router)


@app.get("/")
def root():
    """Comprueba que la API está activa (público, sin JWT)."""
    return {"message": "API Lotería funcionando"}
