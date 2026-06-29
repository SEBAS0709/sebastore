"""
Script para crear usuario administrador inicial
---------------------------------------------------
Ejecutar este script una sola vez para crear un usuario admin
por defecto que se puede usar para acceder al panel administrativo.

Uso: python create_admin.py
"""
from app.database import Base, engine, SessionLocal
from app.models.usuario import Usuario


def crear_admin_inicial():
    """Crea un usuario administrador por defecto si no existe"""
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Verificar si ya existe un admin
    admin_existente = db.query(Usuario).filter(Usuario.rol == "admin").first()
    
    if admin_existente:
        print("✓ Ya existe un usuario administrador en la base de datos.")
        print(f"  Usuario: {admin_existente.nombre_usuario}")
        db.close()
        return
    
    # Crear usuario admin inicial
    admin = Usuario(
        nombre_usuario="admin",
        email="admin@sebastore.local",
        contraseña_hash=Usuario.hash_password("admin123"),
        rol="admin"
    )
    
    db.add(admin)
    db.commit()
    
    print("✓ Usuario administrador creado exitosamente!")
    print("  Credenciales de acceso:")
    print("  • Usuario: admin")
    print("  • Contraseña: admin123")
    print("\n  ⚠️  IMPORTANTE: Cambia esta contraseña inmediatamente después de entrar.")
    
    db.close()


if __name__ == "__main__":
    crear_admin_inicial()
