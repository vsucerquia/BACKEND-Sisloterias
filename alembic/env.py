import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context

load_dotenv()

from database.database import Base  # noqa: E402
from entities.api_usuario import ApiUsuario  # noqa: E402, F401
from entities.boleto import Boleto  # noqa: E402, F401
from entities.juego import Juego  # noqa: E402, F401
from entities.jugador import Jugador  # noqa: E402, F401
from entities.pago import Pago  # noqa: E402, F401
from entities.premio import Premio  # noqa: E402, F401
from entities.sorteo import Sorteo  # noqa: E402, F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL es obligatoria para Alembic.")
    return url


def run_migrations_offline() -> None:
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
