from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from database.database import get_db
from dependencies.auth import get_current_user
from entities.juego import Juego
from schemas.juego_schema import JuegoCreate, JuegoResponse, JuegoUpdate

router = APIRouter(
    prefix="/juegos",
    tags=["Juegos"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[JuegoResponse])
def listar_juegos(db: Session = Depends(get_db)):
    return db.query(Juego).all()


@router.get("/{juego_id}", response_model=JuegoResponse)
def obtener_juego(juego_id: int, db: Session = Depends(get_db)):

    juego = db.query(Juego).filter(Juego.id_juego == juego_id).first()

    if not juego:
        raise NotFoundException("Juego no encontrado")

    return juego


@router.post("/", response_model=JuegoResponse, status_code=201)
def crear_juego(data: JuegoCreate, db: Session = Depends(get_db)):

    nuevo = Juego(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.put("/{juego_id}", response_model=JuegoResponse)
def actualizar_juego(juego_id: int, data: JuegoUpdate, db: Session = Depends(get_db)):

    juego = db.query(Juego).filter(Juego.id_juego == juego_id).first()

    if not juego:
        raise NotFoundException("Juego no encontrado")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(juego, key, value)

    db.commit()
    db.refresh(juego)

    return juego


@router.delete("/{juego_id}")
def eliminar_juego(juego_id: int, db: Session = Depends(get_db)):

    juego = db.query(Juego).filter(Juego.id_juego == juego_id).first()

    if not juego:
        raise NotFoundException("Juego no encontrado")

    db.delete(juego)
    db.commit()

    return {"message": "Juego eliminado"}
