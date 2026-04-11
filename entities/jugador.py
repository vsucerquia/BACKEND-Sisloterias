from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class Jugador(Base):
    __tablename__ = "jugadores"

    id_jugador = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    telefono = Column(String(30), nullable=True)

    boletos = relationship("Boleto", back_populates="jugador")
