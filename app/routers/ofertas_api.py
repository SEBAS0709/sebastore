
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.services.oferta_service import OfertaService
from app.schemas.schemas import OfertaOut, OfertaCreate, OfertaUpdate

router = APIRouter(prefix="/api/ofertas", tags=["Ofertas"])


@router.get("/", response_model=List[OfertaOut])
def listar_ofertas(
    skip: int = 0, limit: int = 60,
    tienda_id: Optional[int] = None,
    buscar: Optional[str] = None,
    orden: str = "descuento",
    solo_activas: bool = True,
    db: Session = Depends(get_db),
):
    """Consultar: lista de ofertas con filtros (tienda, búsqueda, orden)."""
    return OfertaService(db).listar(
        skip=skip, limit=limit, tienda_id=tienda_id,
        buscar=buscar, orden=orden, solo_activas=solo_activas,
    )


@router.get("/{oferta_id}", response_model=OfertaOut)
def obtener_oferta(oferta_id: int, db: Session = Depends(get_db)):
    """Consultar: detalle de una oferta."""
    return OfertaService(db).obtener(oferta_id)


@router.post("/", response_model=OfertaOut, status_code=201)
def crear_oferta(datos: OfertaCreate, db: Session = Depends(get_db)):
    """Registrar una nueva oferta manualmente."""
    return OfertaService(db).crear(datos)


@router.put("/{oferta_id}", response_model=OfertaOut)
def editar_oferta(oferta_id: int, datos: OfertaUpdate, db: Session = Depends(get_db)):
    """Editar una oferta existente."""
    return OfertaService(db).actualizar(oferta_id, datos)


@router.delete("/{oferta_id}", status_code=204)
def eliminar_oferta(oferta_id: int, db: Session = Depends(get_db)):
    """Eliminar una oferta."""
    OfertaService(db).eliminar(oferta_id)
