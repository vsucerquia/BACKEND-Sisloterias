from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from database.database import get_db
from dependencies.auth import get_current_user
from entities.boleto import Boleto
from schemas.boleto_schema import BoletoCreate, BoletoResponse, BoletoUpdate

router = APIRouter(
    prefix="/boletos",
    tags=["Boletos"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[BoletoResponse])
def listar_boletos(db: Session = Depends(get_db)):
    return db.query(Boleto).all()


@router.get("/{boleto_id}", response_model=BoletoResponse)
def obtener_boleto(boleto_id: int, db: Session = Depends(get_db)):
    boleto = db.query(Boleto).filter(Boleto.id_boleto == boleto_id).first()
    if not boleto:
        raise NotFoundException("Boleto no encontrado")
    return boleto


@router.post("/", response_model=BoletoResponse, status_code=201)
def crear_boleto(data: BoletoCreate, db: Session = Depends(get_db)):

    nuevo = Boleto(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.put("/{boleto_id}", response_model=BoletoResponse)
def actualizar_boleto(boleto_id: int, data: BoletoUpdate, db: Session = Depends(get_db)):
    boleto = db.query(Boleto).filter(Boleto.id_boleto == boleto_id).first()
    if not boleto:
        raise NotFoundException("Boleto no encontrado")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(boleto, key, value)

    db.commit()
    db.refresh(boleto)
    return boleto


@router.delete("/{boleto_id}")
def eliminar_boleto(boleto_id: int, db: Session = Depends(get_db)):
    boleto = db.query(Boleto).filter(Boleto.id_boleto == boleto_id).first()
    if not boleto:
        raise NotFoundException("Boleto no encontrado")

    db.delete(boleto)
    db.commit()
    return {"message": "Boleto eliminado"}
