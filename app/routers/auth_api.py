"""
Router de autenticación
---------------------------------------------------
Rutas para login, registro y logout.
"""
from fastapi import APIRouter, Depends, Form, Request, Response, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService

router = APIRouter(tags=["Autenticación"])
templates = Jinja2Templates(directory="app/templates")


def obtener_usuario_actual(request: Request, db: Session = Depends(get_db)):
    """Dependency que obtiene el usuario autenticado de la cookie"""
    token = request.cookies.get("token")
    if not token:
        return None
    
    try:
        auth_service = AuthService(db)
        usuario_id = auth_service.verificar_token(token)
        usuario = auth_service.obtener_usuario_por_id(usuario_id)
        return usuario
    except:
        return None


@router.get("/login")
def login_form(request: Request):
    """Mostrar formulario de login"""
    usuario_actual = obtener_usuario_actual(request, Depends(get_db))
    if usuario_actual:
        return RedirectResponse("/", status_code=303)
    
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(
    nombre_usuario: str = Form(...),
    contraseña: str = Form(...),
    db: Session = Depends(get_db),
):
    """Procesar login"""
    auth_service = AuthService(db)
    usuario = auth_service.autenticar_usuario(nombre_usuario, contraseña)
    token = auth_service.generar_token(usuario.id)
    
    response = RedirectResponse("/", status_code=303)
    response.set_cookie("token", token, max_age=86400)  # 24 horas
    return response


@router.get("/registro")
def registro_form(request: Request):
    """Mostrar formulario de registro"""
    return templates.TemplateResponse("registro.html", {"request": request})


@router.post("/registro")
def registro(
    nombre_usuario: str = Form(...),
    email: str = Form(...),
    contraseña: str = Form(...),
    confirmar_contraseña: str = Form(...),
    db: Session = Depends(get_db),
):
    """Procesar registro de nuevo usuario"""
    if contraseña != confirmar_contraseña:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas no coinciden"
        )
    
    if len(contraseña) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 6 caracteres"
        )
    
    auth_service = AuthService(db)
    try:
        usuario = auth_service.registrar_usuario(nombre_usuario, email, contraseña)
        token = auth_service.generar_token(usuario.id)
        
        response = RedirectResponse("/", status_code=303)
        response.set_cookie("token", token, max_age=86400)
        return response
    except HTTPException as e:
        raise e


@router.get("/logout")
def logout():
    """Cerrar sesión"""
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("token")
    return response
