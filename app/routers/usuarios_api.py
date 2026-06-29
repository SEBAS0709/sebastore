"""
API REST para usuarios
---------------------------------------------------
Endpoints protegidos para gestión de usuarios (admin only).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService
from app.models.usuario import Usuario
from app.schemas.user_schemas import UsuarioRespuesta, UsuarioRegistro
from typing import List

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])


def obtener_usuario_actual(request, db: Session = Depends(get_db)):
    """Obtiene el usuario autenticado desde el request"""
    from fastapi import Request
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )
    
    auth_service = AuthService(db)
    try:
        usuario_id = auth_service.verificar_token(token)
        usuario = auth_service.obtener_usuario_por_id(usuario_id)
        return usuario
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


@router.get("/", response_model=List[UsuarioRespuesta])
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Listar todos los usuarios (solo para administradores)
    
    **Requiere autenticación y rol de administrador**
    """
    if not usuario_actual.es_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden ver la lista de usuarios"
        )
    
    usuarios = db.query(Usuario).all()
    return usuarios


@router.get("/me", response_model=UsuarioRespuesta)
def obtener_perfil(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    """
    Obtener perfil del usuario autenticado
    
    **Requiere autenticación**
    """
    return usuario_actual


@router.get("/{usuario_id}", response_model=UsuarioRespuesta)
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Obtener datos de un usuario específico
    
    **Requiere autenticación (solo puede ver su propio perfil o ser admin)**
    """
    # Si no es admin, solo puede ver su propio perfil
    if not usuario_actual.es_admin() and usuario_actual.id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes acceder al perfil de otros usuarios"
        )
    
    auth_service = AuthService(db)
    usuario = auth_service.obtener_usuario_por_id(usuario_id)
    return usuario
