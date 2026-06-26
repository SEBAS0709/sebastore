"""
Script de datos de ejemplo (DEMO)
---------------------------------------------------
Útil para probar el CRUD y el catálogo SIN depender de internet.
La recolección real de ofertas (botón "Recolectar ofertas") sí
necesita conexión a internet para llegar a la API de CheapShark.

Uso:
    python seed_data.py
"""
from app.database import Base, engine, SessionLocal
from app.models.models import Tienda, Juego, Oferta

Base.metadata.create_all(bind=engine)
db = SessionLocal()

tiendas_demo = [
    Tienda(nombre="Steam", logo_url="https://upload.wikimedia.org/wikipedia/commons/c/cb/Steam_icon_logo.svg"),
    Tienda(nombre="GOG", logo_url=None),
    Tienda(nombre="Epic Games Store", logo_url=None),
    Tienda(nombre="Humble Bundle", logo_url=None),
]
for t in tiendas_demo:
    existe = db.query(Tienda).filter_by(nombre=t.nombre).first()
    if not existe:
        db.add(t)
db.commit()

juegos_demo = [
    {"titulo": "Hollow Knight", "imagen_url": "https://via.placeholder.com/300x170/1F232C/6BFF8E?text=Hollow+Knight", "metacritic_score": 90},
    {"titulo": "Stardew Valley", "imagen_url": "https://via.placeholder.com/300x170/1F232C/6BFF8E?text=Stardew+Valley", "metacritic_score": 89},
    {"titulo": "Hades", "imagen_url": "https://via.placeholder.com/300x170/1F232C/6BFF8E?text=Hades", "metacritic_score": 93},
    {"titulo": "Cyberpunk 2077", "imagen_url": "https://via.placeholder.com/300x170/1F232C/6BFF8E?text=Cyberpunk+2077", "metacritic_score": 86},
]
for jd in juegos_demo:
    existe = db.query(Juego).filter_by(titulo=jd["titulo"]).first()
    if not existe:
        db.add(Juego(**jd))
db.commit()

juegos = db.query(Juego).all()
tiendas = db.query(Tienda).all()

ofertas_demo = [
    (0, 0, 14.99, 4.49, 70, 9.2),
    (1, 1, 13.99, 6.99, 50, 8.5),
    (2, 2, 24.99, 14.99, 40, 9.0),
    (3, 3, 59.99, 23.99, 60, 7.8),
]
for ji, ti, pn, po, desc, rating in ofertas_demo:
    juego = juegos[ji]
    tienda = tiendas[ti]
    existe = db.query(Oferta).filter_by(juego_id=juego.id, tienda_id=tienda.id).first()
    if not existe:
        db.add(Oferta(
            juego_id=juego.id, tienda_id=tienda.id,
            precio_normal=pn, precio_oferta=po,
            porcentaje_descuento=desc, calificacion_oferta=rating,
            url_oferta="#", activa=True,
        ))
db.commit()
db.close()

print("Datos de ejemplo insertados correctamente.")
