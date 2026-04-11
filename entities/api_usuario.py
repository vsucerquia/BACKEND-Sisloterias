from sqlalchemy import Column, Integer, String

from database.database import Base


class ApiUsuario(Base):
    """Usuario para autenticación JWT (no confundir con Jugador)."""

    __tablename__ = "api_usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
