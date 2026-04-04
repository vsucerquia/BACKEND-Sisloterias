from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class JugadorBase(BaseModel):
    nombre: str
    email: EmailStr


class JugadorCreate(JugadorBase):
    pass


class JugadorUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None


class JugadorResponse(JugadorBase):
    id_jugador: int
    fecha_registro: datetime

    class Config:
        from_attributes = True