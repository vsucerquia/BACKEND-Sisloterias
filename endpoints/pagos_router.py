from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from dependencies.auth import get_current_user
from entities.pago import Pago
from schemas.pago_schema import PagoCreate, PagoResponse

router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[PagoResponse])
def listar_pagos(db: Session = Depends(get_db)):
    return db.query(Pago).all()


@router.post("/", response_model=PagoResponse, status_code=201)
def crear_pago(data: PagoCreate, db: Session = Depends(get_db)):

    nuevo = Pago(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo
