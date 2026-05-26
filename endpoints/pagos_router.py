from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from database.database import get_db
from dependencies.auth import get_current_user
from entities.pago import Pago
from schemas.pago_schema import PagoCreate, PagoResponse, PagoUpdate

router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[PagoResponse])
def listar_pagos(db: Session = Depends(get_db)):
    return db.query(Pago).all()


@router.get("/{pago_id}", response_model=PagoResponse)
def obtener_pago(pago_id: int, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id_pago == pago_id).first()
    if not pago:
        raise NotFoundException("Pago no encontrado")
    return pago


@router.post("/", response_model=PagoResponse, status_code=201)
def crear_pago(data: PagoCreate, db: Session = Depends(get_db)):

    nuevo = Pago(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.put("/{pago_id}", response_model=PagoResponse)
def actualizar_pago(pago_id: int, data: PagoUpdate, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id_pago == pago_id).first()
    if not pago:
        raise NotFoundException("Pago no encontrado")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(pago, key, value)

    db.commit()
    db.refresh(pago)
    return pago


@router.delete("/{pago_id}")
def eliminar_pago(pago_id: int, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id_pago == pago_id).first()
    if not pago:
        raise NotFoundException("Pago no encontrado")

    db.delete(pago)
    db.commit()
    return {"message": "Pago eliminado"}
