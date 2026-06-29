"""
Router para el dashboard administrativo
---------------------------------------------------
Muestra métricas clave y estadísticas del negocio.
"""
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.stats_service import StatsService
from app.services.auth_service import AuthService

router = APIRouter(prefix="/admin", tags=["Dashboard"])
templates = Jinja2Templates(directory="app/templates")


def obtener_usuario_desde_request(request: Request, db: Session = Depends(get_db)):
    """Obtiene el usuario autenticado desde la cookie del request"""
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


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    """Página principal del dashboard con métricas"""
    usuario_actual = obtener_usuario_desde_request(request, db)
    stats_service = StatsService(db)
    
    metricas = stats_service.obtener_metricas_generales()
    juegos_populares = stats_service.obtener_juegos_mas_vendidos(limite=8)
    tiendas_populares = stats_service.obtener_tiendas_mas_ofertas(limite=6)
    distribucion_descuentos = stats_service.obtener_distribucion_descuentos()
    vista_base_datos = stats_service.obtener_vista_base_datos(limite=5)
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "metricas": metricas,
            "juegos_populares": juegos_populares,
            "tiendas_populares": tiendas_populares,
            "distribucion_descuentos": distribucion_descuentos,
            "vista_base_datos": vista_base_datos,
            "usuario_actual": usuario_actual,
        },
    )
