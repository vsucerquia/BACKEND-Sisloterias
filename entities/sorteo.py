from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class Sorteo(Base):
    __tablename__ = "sorteos"

    id_sorteo = Column(Integer, primary_key=True, index=True)
    id_juego = Column(Integer, ForeignKey("juegos.id_juego"))
    fecha_sorteo = Column(DateTime)
    numero_ganador = Column(String(50))

    juego = relationship("Juego", back_populates="sorteos")
    boletos = relationship("Boleto", back_populates="sorteo")
