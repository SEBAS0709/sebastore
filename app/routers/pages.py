
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.juego_service import JuegoService
from app.services.oferta_service import OfertaService
from app.repositories.tienda_repository import TiendaRepository
from app.schemas.schemas import JuegoCreate, JuegoUpdate, OfertaCreate, OfertaUpdate

router = APIRouter(tags=["Páginas"])
templates = Jinja2Templates(directory="app/templates")



@router.get("/")
def home(
    request: Request,
    buscar: Optional[str] = None,
    tienda_id: Optional[int] = None,
    orden: str = "descuento",
    db: Session = Depends(get_db),
):
    ofertas = OfertaService(db).listar(
        limit=60, buscar=buscar, tienda_id=tienda_id, orden=orden
    )
    tiendas = TiendaRepository(db).listar()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "ofertas": ofertas,
            "tiendas": tiendas,
            "buscar": buscar or "",
            "tienda_id": tienda_id,
            "orden": orden,
        },
    )


# ---------------------------------------------------------------
# Administración de Juegos (CRUD visual)
# ---------------------------------------------------------------
@router.get("/admin/juegos")
def admin_juegos(request: Request, buscar: Optional[str] = None, db: Session = Depends(get_db)):
    juegos = JuegoService(db).listar(limit=200, buscar=buscar)
    return templates.TemplateResponse(
        "admin_juegos.html",
        {"request": request, "juegos": juegos, "buscar": buscar or ""},
    )


@router.get("/admin/juegos/nuevo")
def nuevo_juego_form(request: Request):
    return templates.TemplateResponse(
        "admin_juego_form.html", {"request": request, "juego": None}
    )


@router.post("/admin/juegos/nuevo")
def crear_juego_form(
    titulo: str = Form(...),
    imagen_url: str = Form(""),
    metacritic_score: str = Form(""),
    db: Session = Depends(get_db),
):
    datos = JuegoCreate(
        titulo=titulo,
        imagen_url=imagen_url or None,
        metacritic_score=int(metacritic_score) if metacritic_score else None,
    )
    JuegoService(db).crear(datos)
    return RedirectResponse("/admin/juegos", status_code=303)


@router.get("/admin/juegos/{juego_id}/editar")
def editar_juego_form(juego_id: int, request: Request, db: Session = Depends(get_db)):
    juego = JuegoService(db).obtener(juego_id)
    return templates.TemplateResponse(
        "admin_juego_form.html", {"request": request, "juego": juego}
    )


@router.post("/admin/juegos/{juego_id}/editar")
def actualizar_juego_form(
    juego_id: int,
    titulo: str = Form(...),
    imagen_url: str = Form(""),
    metacritic_score: str = Form(""),
    db: Session = Depends(get_db),
):
    datos = JuegoUpdate(
        titulo=titulo,
        imagen_url=imagen_url or None,
        metacritic_score=int(metacritic_score) if metacritic_score else None,
    )
    JuegoService(db).actualizar(juego_id, datos)
    return RedirectResponse("/admin/juegos", status_code=303)


@router.post("/admin/juegos/{juego_id}/eliminar")
def eliminar_juego_form(juego_id: int, db: Session = Depends(get_db)):
    JuegoService(db).eliminar(juego_id)
    return RedirectResponse("/admin/juegos", status_code=303)


# ---------------------------------------------------------------
# Administración de Ofertas (CRUD visual)
# ---------------------------------------------------------------
@router.get("/admin/ofertas")
def admin_ofertas(request: Request, db: Session = Depends(get_db)):
    ofertas = OfertaService(db).listar(limit=200, solo_activas=False)
    return templates.TemplateResponse(
        "admin_ofertas.html", {"request": request, "ofertas": ofertas}
    )


@router.get("/admin/ofertas/nuevo")
def nueva_oferta_form(request: Request, db: Session = Depends(get_db)):
    juegos = JuegoService(db).listar(limit=500)
    tiendas = TiendaRepository(db).listar()
    return templates.TemplateResponse(
        "admin_oferta_form.html",
        {"request": request, "oferta": None, "juegos": juegos, "tiendas": tiendas},
    )


@router.post("/admin/ofertas/nuevo")
def crear_oferta_form(
    juego_id: int = Form(...),
    tienda_id: int = Form(...),
    precio_normal: float = Form(...),
    precio_oferta: float = Form(...),
    porcentaje_descuento: float = Form(0),
    db: Session = Depends(get_db),
):
    datos = OfertaCreate(
        juego_id=juego_id,
        tienda_id=tienda_id,
        precio_normal=precio_normal,
        precio_oferta=precio_oferta,
        porcentaje_descuento=porcentaje_descuento,
    )
    OfertaService(db).crear(datos)
    return RedirectResponse("/admin/ofertas", status_code=303)


@router.get("/admin/ofertas/{oferta_id}/editar")
def editar_oferta_form(oferta_id: int, request: Request, db: Session = Depends(get_db)):
    oferta = OfertaService(db).obtener(oferta_id)
    juegos = JuegoService(db).listar(limit=500)
    tiendas = TiendaRepository(db).listar()
    return templates.TemplateResponse(
        "admin_oferta_form.html",
        {"request": request, "oferta": oferta, "juegos": juegos, "tiendas": tiendas},
    )


@router.post("/admin/ofertas/{oferta_id}/editar")
def actualizar_oferta_form(
    oferta_id: int,
    precio_normal: float = Form(...),
    precio_oferta: float = Form(...),
    porcentaje_descuento: float = Form(0),
    activa: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    datos = OfertaUpdate(
        precio_normal=precio_normal,
        precio_oferta=precio_oferta,
        porcentaje_descuento=porcentaje_descuento,
        activa=bool(activa),
    )
    OfertaService(db).actualizar(oferta_id, datos)
    return RedirectResponse("/admin/ofertas", status_code=303)


@router.post("/admin/ofertas/{oferta_id}/eliminar")
def eliminar_oferta_form(oferta_id: int, db: Session = Depends(get_db)):
    OfertaService(db).eliminar(oferta_id)
    return RedirectResponse("/admin/ofertas", status_code=303)
