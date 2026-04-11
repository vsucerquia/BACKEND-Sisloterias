"""Esquema inicial (sin telefono en jugadores).

Revision ID: 001_initial
Revises:
Create Date: 2026-03-27

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import inspect

from alembic import op

revision: str = "001_initial"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    if "juegos" in inspect(bind).get_table_names():
        # Ya existen tablas (p. ej. tras init_db / create_all); no duplicar.
        return

    op.create_table(
        "juegos",
        sa.Column("id_juego", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("tipo", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id_juego"),
    )
    op.create_index(op.f("ix_juegos_id_juego"), "juegos", ["id_juego"], unique=False)

    op.create_table(
        "jugadores",
        sa.Column("id_jugador", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("fecha_registro", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id_jugador"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_jugadores_id_jugador"), "jugadores", ["id_jugador"], unique=False)

    op.create_table(
        "sorteos",
        sa.Column("id_sorteo", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_juego", sa.Integer(), nullable=True),
        sa.Column("fecha_sorteo", sa.DateTime(), nullable=True),
        sa.Column("numero_ganador", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_juego"],
            ["juegos.id_juego"],
        ),
        sa.PrimaryKeyConstraint("id_sorteo"),
    )
    op.create_index(op.f("ix_sorteos_id_sorteo"), "sorteos", ["id_sorteo"], unique=False)

    op.create_table(
        "boletos",
        sa.Column("id_boleto", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_jugador", sa.Integer(), nullable=True),
        sa.Column("id_sorteo", sa.Integer(), nullable=True),
        sa.Column("numero_apostado", sa.String(length=50), nullable=True),
        sa.Column("monto_apuesta", sa.Float(), nullable=True),
        sa.Column("fecha_compra", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_jugador"],
            ["jugadores.id_jugador"],
        ),
        sa.ForeignKeyConstraint(
            ["id_sorteo"],
            ["sorteos.id_sorteo"],
        ),
        sa.PrimaryKeyConstraint("id_boleto"),
    )
    op.create_index(op.f("ix_boletos_id_boleto"), "boletos", ["id_boleto"], unique=False)

    op.create_table(
        "premios",
        sa.Column("id_premio", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_boleto", sa.Integer(), nullable=True),
        sa.Column("monto_premio", sa.Float(), nullable=True),
        sa.Column("estado", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_boleto"],
            ["boletos.id_boleto"],
        ),
        sa.PrimaryKeyConstraint("id_premio"),
        sa.UniqueConstraint("id_boleto"),
    )
    op.create_index(op.f("ix_premios_id_premio"), "premios", ["id_premio"], unique=False)

    op.create_table(
        "pagos",
        sa.Column("id_pago", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_premio", sa.Integer(), nullable=True),
        sa.Column("metodo_pago", sa.String(length=50), nullable=True),
        sa.Column("monto_pagado", sa.Float(), nullable=True),
        sa.Column("fecha_pago", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_premio"],
            ["premios.id_premio"],
        ),
        sa.PrimaryKeyConstraint("id_pago"),
        sa.UniqueConstraint("id_premio"),
    )
    op.create_index(op.f("ix_pagos_id_pago"), "pagos", ["id_pago"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_pagos_id_pago"), table_name="pagos")
    op.drop_table("pagos")
    op.drop_index(op.f("ix_premios_id_premio"), table_name="premios")
    op.drop_table("premios")
    op.drop_index(op.f("ix_boletos_id_boleto"), table_name="boletos")
    op.drop_table("boletos")
    op.drop_index(op.f("ix_sorteos_id_sorteo"), table_name="sorteos")
    op.drop_table("sorteos")
    op.drop_index(op.f("ix_jugadores_id_jugador"), table_name="jugadores")
    op.drop_table("jugadores")
    op.drop_index(op.f("ix_juegos_id_juego"), table_name="juegos")
    op.drop_table("juegos")
