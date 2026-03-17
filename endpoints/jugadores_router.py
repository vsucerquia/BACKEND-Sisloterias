from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db

from entities.jugador import Jugador
from schemas.jugador_schema import (
    JugadorCreate,
    JugadorUpdate,
    JugadorResponse
)

router = APIRouter(prefix="/jugadores", tags=["Jugadores"])


@router.get("/", response_model=list[JugadorResponse])
def listar_jugadores(db: Session = Depends(get_db)):
    return db.query(Jugador).all()


@router.get("/{jugador_id}", response_model=JugadorResponse)
def obtener_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.query(Jugador).filter(Jugador.id_jugador == jugador_id).first()

    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    return jugador


@router.post("/", response_model=JugadorResponse)
def crear_jugador(data: JugadorCreate, db: Session = Depends(get_db)):
    nuevo = Jugador(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.put("/{jugador_id}", response_model=JugadorResponse)
def actualizar_jugador(jugador_id: int, data: JugadorUpdate, db: Session = Depends(get_db)):

    jugador = db.query(Jugador).filter(Jugador.id_jugador == jugador_id).first()

    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(jugador, key, value)

    db.commit()
    db.refresh(jugador)

    return jugador


@router.delete("/{jugador_id}")
def eliminar_jugador(jugador_id: int, db: Session = Depends(get_db)):

    jugador = db.query(Jugador).filter(Jugador.id_jugador == jugador_id).first()

    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    db.delete(jugador)
    db.commit()

    return {"message": "Jugador eliminado"}