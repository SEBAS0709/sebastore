
from sqlalchemy.orm import Session
from app.models.models import Juego


class JuegoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, skip: int = 0, limit: int = 100, buscar: str | None = None):
        query = self.db.query(Juego)
        if buscar:
            query = query.filter(Juego.titulo.ilike(f"%{buscar}%"))
        return query.order_by(Juego.id.desc()).offset(skip).limit(limit).all()

    def obtener_por_id(self, juego_id: int):
        return self.db.query(Juego).filter(Juego.id == juego_id).first()

    def obtener_por_cheapshark_id(self, cheapshark_game_id: str):
        return (
            self.db.query(Juego)
            .filter(Juego.cheapshark_game_id == cheapshark_game_id)
            .first()
        )

    def crear(self, juego: Juego) -> Juego:
        self.db.add(juego)
        self.db.commit()
        self.db.refresh(juego)
        return juego

    def actualizar(self, juego: Juego, datos: dict) -> Juego:
        for campo, valor in datos.items():
            if valor is not None:
                setattr(juego, campo, valor)
        self.db.commit()
        self.db.refresh(juego)
        return juego

    def eliminar(self, juego: Juego) -> None:
        self.db.delete(juego)
        self.db.commit()
