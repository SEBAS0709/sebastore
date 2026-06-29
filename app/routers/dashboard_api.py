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

router = APIRouter(prefix="/admin", tags=["Dashboard"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    """Página principal del dashboard con métricas"""
    stats_service = StatsService(db)
    
    metricas = stats_service.obtener_metricas_generales()
    juegos_populares = stats_service.obtener_juegos_mas_vendidos(limite=8)
    tiendas_populares = stats_service.obtener_tiendas_mas_ofertas(limite=6)
    distribucion_descuentos = stats_service.obtener_distribucion_descuentos()
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "metricas": metricas,
            "juegos_populares": juegos_populares,
            "tiendas_populares": tiendas_populares,
            "distribucion_descuentos": distribucion_descuentos,
        },
    )
