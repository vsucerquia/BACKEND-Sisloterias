from typing import Optional

from pydantic import BaseModel


class PremioBase(BaseModel):
    id_boleto: int
    monto_premio: float
    estado: str


class PremioCreate(PremioBase):
    pass


class PremioUpdate(BaseModel):
    id_boleto: Optional[int] = None
    monto_premio: Optional[float] = None
    estado: Optional[str] = None


class PremioResponse(PremioBase):
    id_premio: int

    class Config:
        from_attributes = True
