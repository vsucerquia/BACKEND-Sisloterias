from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class Pago(Base):
    __tablename__ = "pagos"

    id_pago = Column(Integer, primary_key=True, index=True)
    id_premio = Column(Integer, ForeignKey("premios.id_premio"), unique=True)
    metodo_pago = Column(String(50))
    monto_pagado = Column(Float)
    fecha_pago = Column(DateTime, default=datetime.utcnow)

    premio = relationship("Premio", back_populates="pago")
