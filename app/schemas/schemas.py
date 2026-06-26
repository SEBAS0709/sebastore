
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ---------- Tienda ----------
class TiendaBase(BaseModel):
    nombre: str
    logo_url: Optional[str] = None
    activa: bool = True


class TiendaOut(TiendaBase):
    id: int
    cheapshark_store_id: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- Juego ----------
class JuegoBase(BaseModel):
    titulo: str
    imagen_url: Optional[str] = None
    metacritic_score: Optional[int] = None


class JuegoCreate(JuegoBase):
    pass


class JuegoUpdate(BaseModel):
    titulo: Optional[str] = None
    imagen_url: Optional[str] = None
    metacritic_score: Optional[int] = None


class JuegoOut(JuegoBase):
    id: int
    cheapshark_game_id: Optional[str] = None
    creado_en: datetime

    class Config:
        from_attributes = True


# ---------- Oferta ----------
class OfertaBase(BaseModel):
    juego_id: int
    tienda_id: int
    precio_normal: float
    precio_oferta: float
    porcentaje_descuento: float
    calificacion_oferta: Optional[float] = None
    url_oferta: Optional[str] = None
    activa: bool = True


class OfertaCreate(OfertaBase):
    pass


class OfertaUpdate(BaseModel):
    precio_normal: Optional[float] = None
    precio_oferta: Optional[float] = None
    porcentaje_descuento: Optional[float] = None
    calificacion_oferta: Optional[float] = None
    url_oferta: Optional[str] = None
    activa: Optional[bool] = None


class OfertaOut(OfertaBase):
    id: int
    actualizada_en: datetime

    class Config:
        from_attributes = True
