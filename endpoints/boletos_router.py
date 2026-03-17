from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from entities.boleto import Boleto
from schemas.boleto_schema import BoletoCreate, BoletoUpdate, BoletoResponse

router = APIRouter(prefix="/boletos", tags=["Boletos"])


@router.get("/", response_model=list[BoletoResponse])
def listar_boletos(db: Session = Depends(get_db)):
    return db.query(Boleto).all()


@router.post("/", response_model=BoletoResponse)
def crear_boleto(data: BoletoCreate, db: Session = Depends(get_db)):

    nuevo = Boleto(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo