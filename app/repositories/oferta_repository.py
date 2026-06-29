
from sqlalchemy.orm import Session, joinedload
from app.models.models import Oferta, Tienda


class OfertaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(
        self,
        skip: int = 0,
        limit: int = 60,
        tienda_id: int | str | None = None,
        buscar: str | None = None,
        solo_activas: bool = True,
        orden: str = "descuento",
    ):
        from app.models.models import Juego  # import local para evitar ciclos

        query = self.db.query(Oferta).options(
            joinedload(Oferta.juego), joinedload(Oferta.tienda)
        )
        if solo_activas:
            query = query.filter(Oferta.activa == True)  # noqa: E712
        if tienda_id not in (None, ""):
            tienda_id_str = str(tienda_id)
            try:
                tienda_id_int = int(tienda_id_str)
            except ValueError:
                tienda_id_int = None

            if tienda_id_int is not None:
                query = query.filter(Oferta.tienda_id == tienda_id_int)
            else:
                query = query.filter(
                    Oferta.tienda.has(Tienda.cheapshark_store_id == tienda_id_str)
                )
        if buscar:
            query = query.join(Juego).filter(Juego.titulo.ilike(f"%{buscar}%"))

        if orden == "descuento":
            query = query.order_by(Oferta.porcentaje_descuento.desc())
        elif orden == "precio":
            query = query.order_by(Oferta.precio_oferta.asc())
        elif orden == "rating":
            query = query.order_by(Oferta.calificacion_oferta.desc())

        return query.offset(skip).limit(limit).all()

    def obtener_por_id(self, oferta_id: int):
        return self.db.query(Oferta).filter(Oferta.id == oferta_id).first()

    def obtener_por_juego_y_tienda(self, juego_id: int, tienda_id: int):
        return (
            self.db.query(Oferta)
            .filter(Oferta.juego_id == juego_id, Oferta.tienda_id == tienda_id)
            .first()
        )

    def crear(self, oferta: Oferta) -> Oferta:
        self.db.add(oferta)
        self.db.commit()
        self.db.refresh(oferta)
        return oferta

    def actualizar(self, oferta: Oferta, datos: dict) -> Oferta:
        for campo, valor in datos.items():
            if valor is not None:
                setattr(oferta, campo, valor)
        self.db.commit()
        self.db.refresh(oferta)
        return oferta

    def eliminar(self, oferta: Oferta) -> None:
        self.db.delete(oferta)
        self.db.commit()
