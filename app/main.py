"""
PUNTO DE ENTRADA DE LA APLICACIÓN
---------------------------------------------------
Aquí se inicializa FastAPI, se crean las tablas en la base de datos
(si no existen) y se "enchufan" todos los routers de la capa de
presentación.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.models import models  # noqa: F401 - necesario para registrar las tablas

from app.routers import pages, juegos_api, ofertas_api, sync_api, export_api, dashboard_api, auth_api

# Crea las tablas en SQLite si todavía no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SebaStore - Agregador de ofertas de videojuegos",
    description="Proyecto de examen: arquitectura en capas + CRUD + motor de BD",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Páginas HTML (presentación visual)
app.include_router(pages.router)

# API REST (presentación / integración)
app.include_router(juegos_api.router)
app.include_router(ofertas_api.router)
app.include_router(sync_api.router)
app.include_router(export_api.router)
app.include_router(dashboard_api.router)

# Autenticación
app.include_router(auth_api.router)
