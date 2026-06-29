"""
Servicio de autenticación
---------------------------------------------------
Maneja login, registro y verificación de sesiones.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import jwt
from app.models.usuario import Usuario

SECRET_KEY = "tu-clave-secreta-super-segura-cambiar-en-produccion"
ALGORITHM = "HS256"
EXPIRACION_TOKEN = 24  # horas


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def registrar_usuario(self, nombre_usuario: str, email: str, contraseña: str, es_admin: bool = False) -> Usuario:
        """Registra un nuevo usuario"""
        # Verificar que no exista
        existente = self.db.query(Usuario).filter(
            (Usuario.nombre_usuario == nombre_usuario) | (Usuario.email == email)
        ).first()
        
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario o email ya existe"
            )

        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario,
            email=email,
            contraseña_hash=Usuario.hash_password(contraseña),
            rol="admin" if es_admin else "cliente"
        )
        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)
        return nuevo_usuario

    def autenticar_usuario(self, nombre_usuario: str, contraseña: str) -> Usuario:
        """Autentica un usuario y retorna su objeto si es válido"""
        usuario = self.db.query(Usuario).filter(
            Usuario.nombre_usuario == nombre_usuario
        ).first()

        if not usuario or not usuario.verificar_password(contraseña):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nombre de usuario o contraseña incorrectos",
            )

        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario desactivado"
            )

        return usuario

    def generar_token(self, usuario_id: int) -> str:
        """Genera un JWT token para el usuario"""
        expira = datetime.utcnow() + timedelta(hours=EXPIRACION_TOKEN)
        payload = {
            "usuario_id": usuario_id,
            "exp": expira,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    def verificar_token(self, token: str) -> int:
        """Verifica un token y retorna el usuario_id"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            usuario_id = payload.get("usuario_id")
            if usuario_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido"
                )
            return usuario_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

    def obtener_usuario_por_id(self, usuario_id: int) -> Usuario:
        """Obtiene un usuario por ID"""
        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return usuario
