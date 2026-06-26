"""
CAPA DE DATOS - Configuración de la base de datos
---------------------------------------------------
Aquí se define el motor de base de datos (SQLite) y la fábrica de sesiones
que usará el resto de la aplicación para hablar con la BD.

Si en el futuro se quiere migrar a PostgreSQL o MySQL, solo se cambia
la variable DATABASE_URL (gracias a que usamos SQLAlchemy como ORM).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Motor de BdD: SQLite (un solo archivo, ideal para desarrollo/examen)
DATABASE_URL = "sqlite:///./sebastore.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # necesario para SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de la que heredarán todos los modelos ORM (capa de modelos)
Base = declarative_base()


def get_db():
    """
    Dependencia de FastAPI: abre una sesión de BD por request y
    la cierra automáticamente al terminar (patrón muy común en FastAPI).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
