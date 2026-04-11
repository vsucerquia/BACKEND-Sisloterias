from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from dependencies.auth import get_current_user
from entities.boleto import Boleto
from schemas.boleto_schema import BoletoCreate, BoletoResponse

router = APIRouter(
    prefix="/boletos",
    tags=["Boletos"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[BoletoResponse])
def listar_boletos(db: Session = Depends(get_db)):
    return db.query(Boleto).all()


@router.post("/", response_model=BoletoResponse, status_code=201)
def crear_boleto(data: BoletoCreate, db: Session = Depends(get_db)):

    nuevo = Boleto(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo
