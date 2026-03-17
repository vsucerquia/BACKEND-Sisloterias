from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BoletoBase(BaseModel):
    id_jugador: int
    id_sorteo: int
    numero_apostado: str
    monto_apuesta: float


class BoletoCreate(BoletoBase):
    pass


class BoletoUpdate(BaseModel):
    id_jugador: Optional[int] = None
    id_sorteo: Optional[int] = None
    numero_apostado: Optional[str] = None
    monto_apuesta: Optional[float] = None


class BoletoResponse(BoletoBase):
    id_boleto: int
    fecha_compra: datetime

    class Config:
        from_attributes = True