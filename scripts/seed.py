"""Seeder idempotente: datos iniciales y usuario API para JWT.

Ejecutar tras ``alembic upgrade head``::

    python -m scripts.seed

Variables opcionales (ver .env.example): SEED_ADMIN_USER, SEED_ADMIN_PASSWORD.
"""

import os

from dotenv import load_dotenv
from sqlalchemy.orm import Session

load_dotenv()

from database.database import SessionLocal  # noqa: E402
from entities.api_usuario import ApiUsuario  # noqa: E402
from entities.boleto import Boleto  # noqa: E402, F401
from entities.juego import Juego  # noqa: E402
from entities.jugador import Jugador  # noqa: E402, F401
from entities.pago import Pago  # noqa: E402, F401
from entities.premio import Premio  # noqa: E402, F401
from entities.sorteo import Sorteo  # noqa: E402, F401
from utils.security import hash_password  # noqa: E402


def seed_juego_si_no_existe(db: Session) -> None:
    existe = db.query(Juego).filter(Juego.nombre == "Quiniela nacional").first()
    if existe:
        return
    db.add(Juego(nombre="Quiniela nacional", tipo="numeros"))
    db.commit()


def seed_api_usuario_si_no_existe(db: Session) -> None:
    username = os.getenv("SEED_ADMIN_USER", "admin")
    if db.query(ApiUsuario).filter(ApiUsuario.username == username).first():
        return
    password = os.getenv("SEED_ADMIN_PASSWORD", "admin123")
    db.add(
        ApiUsuario(
            username=username,
            password_hash=hash_password(password),
        )
    )
    db.commit()


def run() -> None:
    db = SessionLocal()
    try:
        seed_juego_si_no_existe(db)
        seed_api_usuario_si_no_existe(db)
        print("Seeder completado (idempotente).")
    finally:
        db.close()


if __name__ == "__main__":
    run()
