from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SorteoBase(BaseModel):
    id_juego: int
    fecha_sorteo: datetime
    numero_ganador: str


class SorteoCreate(SorteoBase):
    pass


class SorteoUpdate(BaseModel):
    id_juego: Optional[int] = None
    fecha_sorteo: Optional[datetime] = None
    numero_ganador: Optional[str] = None


class SorteoResponse(SorteoBase):
    id_sorteo: int

    class Config:
        from_attributes = True