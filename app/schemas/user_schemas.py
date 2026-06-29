"""
Schemas adicionales para validación de API
---------------------------------------------------
Define estructuras de datos para validación con Pydantic.
"""
from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class UsuarioRegistro(BaseModel):
    nombre_usuario: str
    email: EmailStr
    contraseña: str
    
    @validator('nombre_usuario')
    def nombre_usuario_valido(cls, v):
        if len(v) < 3:
            raise ValueError('El nombre de usuario debe tener al menos 3 caracteres')
        if not v.isalnum():
            raise ValueError('El nombre de usuario solo puede contener letras y números')
        return v
    
    @validator('contraseña')
    def contraseña_valida(cls, v):
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v


class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contraseña: str


class UsuarioRespuesta(BaseModel):
    id: int
    nombre_usuario: str
    email: str
    rol: str
    activo: bool
    
    class Config:
        from_attributes = True


class JuegoRespuesta(BaseModel):
    id: int
    titulo: str
    imagen_url: Optional[str] = None
    metacritic_score: Optional[int] = None
    
    class Config:
        from_attributes = True


class OfertaRespuesta(BaseModel):
    id: int
    juego_id: int
    tienda_id: int
    precio_normal: float
    precio_oferta: float
    porcentaje_descuento: float
    calificacion_oferta: Optional[float] = None
    activa: bool
    
    class Config:
        from_attributes = True
