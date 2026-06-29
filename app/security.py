"""
Middleware y decoradores para proteger rutas administrativas
---------------------------------------------------
Asegura que solo administradores puedan acceder a ciertas rutas.
"""
from fastapi import HTTPException, status, Request
from app.services.auth_service import AuthService
from sqlalchemy.orm import Session


def requerir_admin(request: Request, db: Session, auth_service: AuthService = None):
    """
    Verifica que el usuario actual sea administrador.
    Levanta HTTPException 403 si no lo es.
    """
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No estás autenticado"
        )
    
    if auth_service is None:
        auth_service = AuthService(db)
    
    try:
        usuario_id = auth_service.verificar_token(token)
        usuario = auth_service.obtener_usuario_por_id(usuario_id)
        
        if not usuario.es_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo administradores pueden acceder a esta sección"
            )
        
        return usuario
    except HTTPException:
        raise
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
