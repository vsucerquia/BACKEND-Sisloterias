from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class Premio(Base):
    __tablename__ = "premios"

    id_premio = Column(Integer, primary_key=True, index=True)
    id_boleto = Column(Integer, ForeignKey("boletos.id_boleto"), unique=True)
    monto_premio = Column(Float)
    estado = Column(String(50), default="pendiente")

    boleto = relationship("Boleto", back_populates="premio")
    pago = relationship("Pago", back_populates="premio", uselist=False)
