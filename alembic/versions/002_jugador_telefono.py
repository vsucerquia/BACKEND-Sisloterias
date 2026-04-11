"""Añade columna telefono a jugadores.

Revision ID: 002_jugador_telefono
Revises: 001_initial
Create Date: 2026-03-27

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import inspect

from alembic import op

revision: str = "002_jugador_telefono"
down_revision: Union[str, Sequence[str], None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if "jugadores" not in inspector.get_table_names():
        return
    cols = {c["name"] for c in inspector.get_columns("jugadores")}
    if "telefono" in cols:
        return
    op.add_column("jugadores", sa.Column("telefono", sa.String(length=30), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    if "jugadores" not in inspector.get_table_names():
        return
    cols = {c["name"] for c in inspector.get_columns("jugadores")}
    if "telefono" not in cols:
        return
    op.drop_column("jugadores", "telefono")
