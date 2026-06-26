
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.services.juego_service import JuegoService
from app.schemas.schemas import JuegoOut, JuegoCreate, JuegoUpdate

router = APIRouter(prefix="/api/juegos", tags=["Juegos"])


@router.get("/", response_model=List[JuegoOut])
def listar_juegos(
    skip: int = 0, limit: int = 100, buscar: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Consultar: lista de juegos, con búsqueda opcional por título."""
    return JuegoService(db).listar(skip=skip, limit=limit, buscar=buscar)


@router.get("/{juego_id}", response_model=JuegoOut)
def obtener_juego(juego_id: int, db: Session = Depends(get_db)):
    """Consultar: detalle de un juego."""
    return JuegoService(db).obtener(juego_id)


@router.post("/", response_model=JuegoOut, status_code=201)
def crear_juego(datos: JuegoCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo juego."""
    return JuegoService(db).crear(datos)


@router.put("/{juego_id}", response_model=JuegoOut)
def editar_juego(juego_id: int, datos: JuegoUpdate, db: Session = Depends(get_db)):
    """Editar un juego existente."""
    return JuegoService(db).actualizar(juego_id, datos)


@router.delete("/{juego_id}", status_code=204)
def eliminar_juego(juego_id: int, db: Session = Depends(get_db)):
    """Eliminar un juego."""
    JuegoService(db).eliminar(juego_id)
