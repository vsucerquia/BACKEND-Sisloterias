from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from database.database import get_db
from dependencies.auth import get_current_user
from entities.premio import Premio
from schemas.premio_schema import PremioCreate, PremioResponse, PremioUpdate

router = APIRouter(
    prefix="/premios",
    tags=["Premios"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[PremioResponse])
def listar_premios(db: Session = Depends(get_db)):
    return db.query(Premio).all()


@router.get("/{premio_id}", response_model=PremioResponse)
def obtener_premio(premio_id: int, db: Session = Depends(get_db)):
    premio = db.query(Premio).filter(Premio.id_premio == premio_id).first()
    if not premio:
        raise NotFoundException("Premio no encontrado")
    return premio


@router.post("/", response_model=PremioResponse, status_code=201)
def crear_premio(data: PremioCreate, db: Session = Depends(get_db)):

    nuevo = Premio(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.put("/{premio_id}", response_model=PremioResponse)
def actualizar_premio(premio_id: int, data: PremioUpdate, db: Session = Depends(get_db)):
    premio = db.query(Premio).filter(Premio.id_premio == premio_id).first()
    if not premio:
        raise NotFoundException("Premio no encontrado")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(premio, key, value)

    db.commit()
    db.refresh(premio)
    return premio


@router.delete("/{premio_id}")
def eliminar_premio(premio_id: int, db: Session = Depends(get_db)):
    premio = db.query(Premio).filter(Premio.id_premio == premio_id).first()
    if not premio:
        raise NotFoundException("Premio no encontrado")

    db.delete(premio)
    db.commit()
    return {"message": "Premio eliminado"}
