"""Database helpers (SQLAlchemy) for the Sisloterias project.

La URL se lee de la variable de entorno ``DATABASE_URL`` (archivo ``.env`` en la raíz
del backend). Para Neon (PostgreSQL), usa la cadena del panel; suele incluir
``?sslmode=require``.

No pegues la connection string en código; solo en ``.env``.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

_root = Path(__file__).resolve().parent.parent
_env_path = _root / ".env"
load_dotenv(_env_path)

DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()
if not DATABASE_URL:
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

connect_args: dict = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides a database session."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
