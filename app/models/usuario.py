"""
Modelo de Usuario con autenticación y roles
---------------------------------------------------
Define el modelo de usuario con soporte para autenticación.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base
import hashlib
import secrets


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    contraseña_hash = Column(String, nullable=False)
    rol = Column(String, default="cliente")  # "admin" o "cliente"
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def hash_password(contraseña: str) -> str:
        """Hash una contraseña usando SHA256 + salt"""
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            contraseña.encode(),
            salt.encode(),
            100000
        )
        return f"{salt}${hashed.hex()}"

    def verificar_password(self, contraseña: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        try:
            salt, stored_hash = self.contraseña_hash.split('$')
            new_hash = hashlib.pbkdf2_hmac(
                'sha256',
                contraseña.encode(),
                salt.encode(),
                100000
            )
            return new_hash.hex() == stored_hash
        except:
            return False

    def es_admin(self) -> bool:
        """Retorna True si el usuario es administrador"""
        return self.rol == "admin"

    def es_cliente(self) -> bool:
        """Retorna True si el usuario es cliente"""
        return self.rol == "cliente"
