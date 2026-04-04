from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PagoBase(BaseModel):
    id_premio: int
    metodo_pago: str
    monto_pagado: float


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    id_premio: Optional[int] = None
    metodo_pago: Optional[str] = None
    monto_pagado: Optional[float] = None


class PagoResponse(PagoBase):
    id_pago: int
    fecha_pago: datetime

    class Config:
        from_attributes = True