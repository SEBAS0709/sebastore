
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Tienda(Base):
    __tablename__ = "tiendas"

    id = Column(Integer, primary_key=True, index=True)
    cheapshark_store_id = Column(String, unique=True, nullable=True, index=True)
    nombre = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)
    activa = Column(Boolean, default=True)

    ofertas = relationship("Oferta", back_populates="tienda")


class Juego(Base):
    __tablename__ = "juegos"

    id = Column(Integer, primary_key=True, index=True)
    cheapshark_game_id = Column(String, unique=True, nullable=True, index=True)
    titulo = Column(String, nullable=False, index=True)
    imagen_url = Column(String, nullable=True)
    metacritic_score = Column(Integer, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    ofertas = relationship(
        "Oferta", back_populates="juego", cascade="all, delete-orphan"
    )


class Oferta(Base):
    __tablename__ = "ofertas"

    id = Column(Integer, primary_key=True, index=True)
    juego_id = Column(Integer, ForeignKey("juegos.id"), nullable=False)
    tienda_id = Column(Integer, ForeignKey("tiendas.id"), nullable=False)

    precio_normal = Column(Float, nullable=False, default=0.0)
    precio_oferta = Column(Float, nullable=False, default=0.0)
    porcentaje_descuento = Column(Float, nullable=False, default=0.0)
    calificacion_oferta = Column(Float, nullable=True)  # dealRating de CheapShark
    url_oferta = Column(Text, nullable=True)

    activa = Column(Boolean, default=True)
    actualizada_en = Column(DateTime, default=datetime.utcnow)

    juego = relationship("Juego", back_populates="ofertas")
    tienda = relationship("Tienda", back_populates="ofertas")
