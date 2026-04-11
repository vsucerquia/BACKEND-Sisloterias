from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from database.database import get_db
from dependencies.auth import get_current_user
from entities.sorteo import Sorteo
from schemas.sorteo_schema import SorteoCreate, SorteoResponse, SorteoUpdate

router = APIRouter(
    prefix="/sorteos",
    tags=["Sorteos"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[SorteoResponse])
def listar_sorteos(db: Session = Depends(get_db)):
    return db.query(Sorteo).all()


@router.get("/{sorteo_id}", response_model=SorteoResponse)
def obtener_sorteo(sorteo_id: int, db: Session = Depends(get_db)):

    sorteo = db.query(Sorteo).filter(Sorteo.id_sorteo == sorteo_id).first()

    if not sorteo:
        raise NotFoundException("Sorteo no encontrado")

    return sorteo


@router.post("/", response_model=SorteoResponse, status_code=201)
def crear_sorteo(data: SorteoCreate, db: Session = Depends(get_db)):

    nuevo = Sorteo(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.put("/{sorteo_id}", response_model=SorteoResponse)
def actualizar_sorteo(sorteo_id: int, data: SorteoUpdate, db: Session = Depends(get_db)):

    sorteo = db.query(Sorteo).filter(Sorteo.id_sorteo == sorteo_id).first()

    if not sorteo:
        raise NotFoundException("Sorteo no encontrado")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(sorteo, key, value)

    db.commit()
    db.refresh(sorteo)

    return sorteo


@router.delete("/{sorteo_id}")
def eliminar_sorteo(sorteo_id: int, db: Session = Depends(get_db)):

    sorteo = db.query(Sorteo).filter(Sorteo.id_sorteo == sorteo_id).first()

    if not sorteo:
        raise NotFoundException("Sorteo no encontrado")

    db.delete(sorteo)
    db.commit()

    return {"message": "Sorteo eliminado"}
