from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from entities.pago import Pago
from schemas.pago_schema import PagoCreate, PagoResponse

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.get("/", response_model=list[PagoResponse])
def listar_pagos(db: Session = Depends(get_db)):
    return db.query(Pago).all()


@router.post("/", response_model=PagoResponse)
def crear_pago(data: PagoCreate, db: Session = Depends(get_db)):

    nuevo = Pago(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo