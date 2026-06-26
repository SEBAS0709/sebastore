# SebaStore — Agregador de ofertas de videojuegos

Proyecto de examen final: catálogo de ofertas de videojuegos (estilo Eneba/Steam)
que recolecta descuentos de Steam, GOG, Epic, Humble y más de 30 tiendas usando
la API pública y gratuita de **CheapShark**.

## Arquitectura en capas

```
Presentación   ->  app/routers/  (páginas HTML + API REST)  +  app/templates + app/static
Lógica negocio ->  app/services/ (reglas de negocio, validaciones, integración externa)
Acceso a datos ->  app/repositories/ (consultas SQLAlchemy)
Modelo/Datos   ->  app/models/ (tablas ORM)  +  app/database.py (motor SQLite)
```

Cada capa solo conoce a la capa inmediatamente inferior:
`router -> service -> repository -> modelo ORM -> base de datos`.
Esto es justo lo que pide la pizarra ("Arquitectura en Capas").

- **Motor de BdD**: SQLite (`sebastore.db`), vía SQLAlchemy. Migrar a
  PostgreSQL/MySQL después solo requiere cambiar `DATABASE_URL` en
  `app/database.py`.
- **Lenguajes**: Python (FastAPI) en el backend, HTML + CSS + JavaScript
  en el frontend (plantillas Jinja2, sin frameworks pesados).
- **CRUD implementado**: Juegos y Ofertas (registrar, editar, eliminar,
  consultar), tanto desde la interfaz web (`/admin/juegos`, `/admin/ofertas`)
  como desde la API REST (`/api/juegos`, `/api/ofertas` — ver `/docs`).
- **Recolección de ofertas**: botón "⟳ Recolectar ofertas" en la barra
  superior, que llama a `/api/sync/cheapshark` y trae las ofertas activas
  desde la API de CheapShark.
- **Reportes (extra)**: exportación a CSV, Excel y PDF desde
  `/admin/ofertas` (botones de descarga).

## Cómo correrlo

```bash
pip install -r requirements.txt
python seed_data.py        # (opcional) datos de ejemplo para probar sin internet
uvicorn app.main:app --reload
```

Abrir http://localhost:8000

- Catálogo público: `/`
- Administrar juegos: `/admin/juegos`
- Administrar ofertas: `/admin/ofertas`
- Documentación interactiva de la API: `/docs`

> El botón "Recolectar ofertas" necesita conexión a internet real (la API
> de CheapShark vive en cheapshark.com). El script `seed_data.py` te deja
> probar todo el CRUD y el catálogo sin depender de internet.

## Plan sugerido (hoy -> martes)

1. **Hoy**: levantar el proyecto, correr `seed_data.py`, probar el CRUD de
   Juegos y Ofertas desde `/admin`, entender las 4 capas.
2. **Sábado/Domingo**: probar el botón "Recolectar ofertas" con internet
   real, revisar que el catálogo (`/`) se llene con ofertas reales,
   ajustar filtros/orden si quieres.
3. **Lunes**: pulir detalles visuales, decidir si entregas también el
   extra de exportación (ya está listo: CSV/Excel/PDF), preparar qué vas
   a explicar de la arquitectura.
4. **Martes**: pruebas finales y entrega.

## Posibles mejoras si te queda tiempo

- Agregar CRUD visual de Tiendas (`Tienda`) — el repositorio ya existe,
  solo falta el router/templates, igual que se hizo con Juego.
- Agregar autenticación simple para `/admin`.
- Guardar histórico de precios por juego (tabla `HistorialPrecio`).
