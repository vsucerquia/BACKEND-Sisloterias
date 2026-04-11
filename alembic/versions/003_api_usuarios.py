"""Tabla api_usuarios para login JWT.

Revision ID: 003_api_usuarios
Revises: 002_jugador_telefono
Create Date: 2026-03-27

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import inspect

from alembic import op

revision: str = "003_api_usuarios"
down_revision: Union[str, Sequence[str], None] = "002_jugador_telefono"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if "api_usuarios" in inspect(op.get_bind()).get_table_names():
        return

    op.create_table(
        "api_usuarios",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_api_usuarios_id"), "api_usuarios", ["id"], unique=False)
    op.create_index(op.f("ix_api_usuarios_username"), "api_usuarios", ["username"], unique=True)


def downgrade() -> None:
    bind = op.get_bind()
    if "api_usuarios" not in inspect(bind).get_table_names():
        return
    op.drop_index(op.f("ix_api_usuarios_username"), table_name="api_usuarios")
    op.drop_index(op.f("ix_api_usuarios_id"), table_name="api_usuarios")
    op.drop_table("api_usuarios")
