"""Configuración de SQLAlchemy: motor, sesión y base declarativa.

La URL de conexión se lee de la variable de entorno ``DATABASE_URL`` (archivo ``.env``).
Para Neon (PostgreSQL), usa la cadena que copias del panel de Neon; suele incluir
``?sslmode=require``.

No pegues la connection string en este archivo Python; solo en ``.env`` (``DATABASE_URL=``).
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Carga .env desde la raíz del proyecto BACKEND-Sisloterias
_root = Path(__file__).resolve().parent.parent
_env_path = _root / ".env"
load_dotenv(_env_path)

SQLALCHEMY_DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()
if not SQLALCHEMY_DATABASE_URL:
    if _env_path.is_file():
        detalle = (
            f"\nEl archivo existe: {_env_path}\n"
            "Pero DATABASE_URL está vacía. Abre .env y en la línea "
            "DATABASE_URL= pega la connection string completa de Neon (sin espacios "
            "antes ni después del =)."
        )
    else:
        detalle = (
            f"\nCrea el archivo: {_env_path}\n"
            "Puedes copiar .env.example a .env y define DATABASE_URL=..."
        )
    raise RuntimeError(
        "DATABASE_URL no está definida."
        + detalle
        + "\nNo subas .env al repositorio."
    )

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Entrega una sesión de base de datos para inyección en FastAPI.

    Yields:
        sqlalchemy.orm.Session: Sesión de base de datos.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
