from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base


class Boleto(Base):
    __tablename__ = "boletos"

    id_boleto = Column(Integer, primary_key=True, index=True)
    id_jugador = Column(Integer, ForeignKey("jugadores.id_jugador"))
    id_sorteo = Column(Integer, ForeignKey("sorteos.id_sorteo"))
    numero_apostado = Column(String(50))
    monto_apuesta = Column(Float)
    fecha_compra = Column(DateTime, default=datetime.utcnow)

    jugador = relationship("Jugador", back_populates="boletos")
    sorteo = relationship("Sorteo", back_populates="boletos")
    premio = relationship("Premio", back_populates="boleto", uselist=False)