
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.models import Juego
from app.repositories.juego_repository import JuegoRepository
from app.schemas.schemas import JuegoCreate, JuegoUpdate


class JuegoService:
    def __init__(self, db: Session):
        self.repo = JuegoRepository(db)

    def listar(self, skip: int = 0, limit: int = 100, buscar: str | None = None):
        return self.repo.listar(skip=skip, limit=limit, buscar=buscar)

    def obtener(self, juego_id: int) -> Juego:
        juego = self.repo.obtener_por_id(juego_id)
        if not juego:
            raise HTTPException(status_code=404, detail="Juego no encontrado")
        return juego

    def crear(self, datos: JuegoCreate) -> Juego:
        if not datos.titulo or not datos.titulo.strip():
            raise HTTPException(status_code=400, detail="El título es obligatorio")
        nuevo = Juego(
            titulo=datos.titulo.strip(),
            imagen_url=datos.imagen_url,
            metacritic_score=datos.metacritic_score,
        )
        return self.repo.crear(nuevo)

    def actualizar(self, juego_id: int, datos: JuegoUpdate) -> Juego:
        juego = self.obtener(juego_id)
        return self.repo.actualizar(juego, datos.model_dump(exclude_unset=True))

    def eliminar(self, juego_id: int) -> None:
        juego = self.obtener(juego_id)
        self.repo.eliminar(juego)
