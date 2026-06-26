
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.models import Oferta
from app.repositories.oferta_repository import OfertaRepository
from app.repositories.juego_repository import JuegoRepository
from app.repositories.tienda_repository import TiendaRepository
from app.schemas.schemas import OfertaCreate, OfertaUpdate


class OfertaService:
    def __init__(self, db: Session):
        self.repo = OfertaRepository(db)
        self.juego_repo = JuegoRepository(db)
        self.tienda_repo = TiendaRepository(db)

    def listar(self, **filtros):
        return self.repo.listar(**filtros)

    def obtener(self, oferta_id: int) -> Oferta:
        oferta = self.repo.obtener_por_id(oferta_id)
        if not oferta:
            raise HTTPException(status_code=404, detail="Oferta no encontrada")
        return oferta

    def _validar_referencias(self, juego_id: int, tienda_id: int):
        if not self.juego_repo.obtener_por_id(juego_id):
            raise HTTPException(status_code=400, detail="El juego no existe")
        if not self.tienda_repo.obtener_por_id(tienda_id):
            raise HTTPException(status_code=400, detail="La tienda no existe")

    def crear(self, datos: OfertaCreate) -> Oferta:
        self._validar_referencias(datos.juego_id, datos.tienda_id)
        if datos.precio_oferta > datos.precio_normal:
            raise HTTPException(
                status_code=400,
                detail="El precio de oferta no puede ser mayor al precio normal",
            )
        nueva = Oferta(**datos.model_dump())
        return self.repo.crear(nueva)

    def actualizar(self, oferta_id: int, datos: OfertaUpdate) -> Oferta:
        oferta = self.obtener(oferta_id)
        return self.repo.actualizar(oferta, datos.model_dump(exclude_unset=True))

    def eliminar(self, oferta_id: int) -> None:
        oferta = self.obtener(oferta_id)
        self.repo.eliminar(oferta)
