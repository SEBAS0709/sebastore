
from sqlalchemy.orm import Session
from app.models.models import Tienda


class TiendaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.query(Tienda).order_by(Tienda.nombre.asc()).all()

    def obtener_por_id(self, tienda_id: int):
        return self.db.query(Tienda).filter(Tienda.id == tienda_id).first()

    def obtener_por_cheapshark_id(self, cheapshark_store_id: str):
        return (
            self.db.query(Tienda)
            .filter(Tienda.cheapshark_store_id == cheapshark_store_id)
            .first()
        )

    def crear(self, tienda: Tienda) -> Tienda:
        self.db.add(tienda)
        self.db.commit()
        self.db.refresh(tienda)
        return tienda
