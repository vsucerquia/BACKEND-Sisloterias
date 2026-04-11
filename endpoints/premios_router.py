from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from dependencies.auth import get_current_user
from entities.premio import Premio
from schemas.premio_schema import PremioCreate, PremioResponse

router = APIRouter(
    prefix="/premios",
    tags=["Premios"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[PremioResponse])
def listar_premios(db: Session = Depends(get_db)):
    return db.query(Premio).all()


@router.post("/", response_model=PremioResponse, status_code=201)
def crear_premio(data: PremioCreate, db: Session = Depends(get_db)):

    nuevo = Premio(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo
