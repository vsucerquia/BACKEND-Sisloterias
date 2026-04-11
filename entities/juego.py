from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class Juego(Base):
    __tablename__ = "juegos"

    id_juego = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)

    sorteos = relationship("Sorteo", back_populates="juego")
