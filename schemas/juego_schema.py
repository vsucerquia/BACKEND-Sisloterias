from typing import Optional

from pydantic import BaseModel


class JuegoBase(BaseModel):
    nombre: str
    tipo: str


class JuegoCreate(JuegoBase):
    pass


class JuegoUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None


class JuegoResponse(JuegoBase):
    id_juego: int

    class Config:
        from_attributes = True
