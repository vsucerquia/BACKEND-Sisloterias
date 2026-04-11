from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class JugadorBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None


class JugadorCreate(JugadorBase):
    pass


class JugadorUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None


class JugadorResponse(JugadorBase):
    id_jugador: int
    fecha_registro: datetime

    class Config:
        from_attributes = True
