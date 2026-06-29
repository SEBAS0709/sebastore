# SebaStore — Agregador Inteligente de Ofertas de Videojuegos

**Proyecto de Examen Final** | Carrera de Sistemas Informáticos | Materia: Diseño y Programación Web II

## 📋 Descripción General

**SebaStore** es un MVP (Producto Mínimo Viable) completamente funcional que agrega y compara ofertas de videojuegos en tiempo real desde más de 30 plataformas digitales (Steam, GOG, Epic Games Store, Humble Bundle y más). Integra la API pública de **CheapShark** para sincronizar datos en vivo, proporciona un catálogo filtrable para usuarios finales, y ofrece un panel administrativo completo con CRUD de juegos, ofertas y reportes exportables.

## ✨ Características Principales

### 🎯 Para Usuarios Finales
- **Catálogo dinámico** de ofertas con búsqueda y filtros por tienda
- **Ordenamiento inteligente**: por descuento, precio o calificación
- **Comparación de precios** en tiempo real entre diferentes plataformas
- **Interfaz responsiva** optimizada para desktop, tablet y móvil

### 🔧 Para Administradores
- **Dashboard de estadísticas** con métricas clave del negocio
  - Total de juegos, tiendas y ofertas activas
  - Ahorro total generado para clientes
  - Juegos y tiendas más populares
  - Distribución de descuentos
- **CRUD visual completo** para Juegos y Ofertas
  - Crear, editar, eliminar, listar
  - Validación robusta de datos
  - Interfaz intuitiva
- **Exportación de reportes**:
  - Formato CSV para importar a hojas de cálculo
  - Formato Excel con estilos automáticos
  - Formato PDF con estructura profesional
- **Sincronización con CheapShark API**: trae ofertas reales automáticamente

## 🏗️ Arquitectura Técnica (Capas)

```
┌─────────────────────────────────────────────────────────┐
│         CAPA DE PRESENTACIÓN (Presentation Layer)       │
│  app/routers/ + app/templates/ + app/static/           │
│  HTML5, CSS3, JavaScript + Jinja2 Templates            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│       CAPA DE LÓGICA DE NEGOCIO (Business Logic)       │
│          app/services/                                  │
│  • JuegoService: reglas de negocio de juegos          │
│  • OfertaService: reglas de oferta y descuentos       │
│  • StatsService: cálculo de métricas                   │
│  • ExportService: formateo de reportes                 │
│  • CheapSharkService: integración con API externa      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│      CAPA DE ACCESO A DATOS (Data Access Layer)        │
│          app/repositories/                              │
│  • JuegoRepository: consultas de juegos               │
│  • OfertaRepository: consultas de ofertas             │
│  • TiendaRepository: consultas de tiendas             │
│  SQLAlchemy ORM queries                                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│           CAPA DE DATOS (Data Layer)                    │
│      app/models/ + app/database.py                     │
│  • SQLAlchemy ORM Models                               │
│  • SQLite Database (sebastore.db)                      │
│  • Migraciones y relaciones de tablas                   │
└─────────────────────────────────────────────────────────┘
```

### Principio de Inversión de Dependencias
Cada capa superior **solo depende** de la capa inmediatamente inferior:
- Router → Service → Repository → ORM Model → Database

Esto asegura **bajo acoplamiento**, **alta cohesión** y facilita testing y mantenimiento.

## 🗄️ Modelo de Datos

### Entidades Principales

**Tienda** (ecommerce platforms)
```
- id (PK)
- nombre (ej: Steam, GOG, Epic)
- logo_url (referencia a logo de tienda)
- cheapshark_store_id (ID externo para sincronización)
- activa (boolean)
```

**Juego** (video games)
```
- id (PK)
- titulo (nombre del juego)
- imagen_url (carátula/cover)
- metacritic_score (puntuación crítica)
- cheapshark_game_id (ID externo para sincronización)
- creado_en (timestamp)
- Relación 1 → N con Ofertas
```

**Oferta** (price deals)
```
- id (PK)
- juego_id (FK → Juego)
- tienda_id (FK → Tienda)
- precio_normal (MSRP)
- precio_oferta (precio actual con descuento)
- porcentaje_descuento (calculado)
- calificacion_oferta (rating de la oferta)
- url_oferta (link directo a la tienda)
- activa (boolean)
- actualizada_en (timestamp)
- Relaciones N → 1 con Juego y Tienda
```

### Relaciones
- **Juego ↔ Oferta**: 1 a N (un juego puede tener muchas ofertas en diferentes tiendas)
- **Tienda ↔ Oferta**: 1 a N (una tienda puede tener muchas ofertas)

## 🚀 Instrucciones de Instalación y Ejecución

### Requisitos Previos
- Python 3.9+
- pip (administrador de paquetes)
- Navegador web moderno

### Pasos de Instalación

#### 1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd gamedeals/gamedeals
```

#### 2. Crear y activar entorno virtual
```bash
# En Windows
python -m venv .venv
.venv\Scripts\activate

# En macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 4. Crear usuario administrador
```bash
python create_admin.py
```

Esto creará un usuario admin con credenciales:
- **Usuario**: `admin`
- **Contraseña**: `admin123`

> ⚠️ Cambia esta contraseña inmediatamente después de entrar al sistema.

#### 5. Inicializar base de datos (opcional: cargar datos de ejemplo)
```bash
python seed_data.py
```

#### 6. Ejecutar el servidor
```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en **http://localhost:8000**

### Rutas Principales

| Ruta | Descripción |
|------|-------------|
| `/` | Catálogo público de ofertas |
| `/login` | 🔐 Iniciar sesión |
| `/registro` | 📝 Crear nueva cuenta |
| `/admin/dashboard` | 📊 Dashboard con métricas (solo admin) |
| `/admin/juegos` | Gestión de juegos (solo admin) |
| `/admin/ofertas` | Gestión de ofertas (solo admin) |
| `/api/juegos` | API REST de juegos |
| `/api/ofertas` | API REST de ofertas |
| `/api/sync/cheapshark` | Sincronizar ofertas desde API externa |
| `/api/export/{csv,excel,pdf}` | Descargar reportes |
| `/docs` | Documentación interactiva Swagger UI |

## 📊 Métricas del Dashboard

El dashboard proporciona análisis en tiempo real:

- **Juegos en catálogo**: total de juegos únicos
- **Tiendas conectadas**: cantidad de plataformas integradas
- **Ofertas activas**: cantidad de precios especiales vigentes
- **Ahorro total**: suma de diferencias (precio normal - precio con descuento)
- **Juegos más populares**: listado de juegos con más ofertas
- **Tiendas más activas**: ranking de plataformas por cantidad de ofertas
- **Distribución de descuentos**: gráfico de barras por rango de descuento

## 🔄 Flujo de Datos

### Sincronización con API Externa (CheapShark)
```
1. Usuario presiona "⟳ Recolectar ofertas"
2. Sistema llama a CheapShark API (/api/sync/cheapshark)
3. Descarga catálogo de juegos y tiendas activas
4. Mapea datos externos a modelos locales
5. Actualiza tablas (Tienda, Juego, Oferta) en SQLite
6. Dashboard se recalcula automáticamente
```

### Validación de Datos
Todos los formularios incluyen validación en dos niveles:
- **Frontend (JavaScript)**: validación inmediata en tiempo de escritura
- **Backend (Pydantic + SQLAlchemy)**: validación antes de guardar en BD

## 💾 Dependencias

| Librería | Versión | Propósito |
|----------|---------|----------|
| `fastapi` | 0.115.0 | Framework web moderno |
| `uvicorn[standard]` | 0.30.6 | Servidor ASGI |
| `sqlalchemy` | 2.0.35 | ORM y herramientas de BD |
| `jinja2` | 3.1.4 | Motor de plantillas |
| `httpx` | 0.27.2 | Cliente HTTP para API externa |
| `openpyxl` | 3.1.5 | Generación de archivos Excel |
| `reportlab` | 4.2.5 | Generación de archivos PDF |

## 🎨 Interfaz y Diseño

### Paleta de Colores
- **Fondo**: Dark mode (#0E1013) para reducir fatiga visual
- **Acentos**: Verde (#6BFF8E) para CTAs y elementos positivos
- **Alertas**: Rojo (#FF5468) para elementos destructivos
- **Información**: Azul (#6C7CFF) para acciones secundarias

### Tipografía
- **Titles**: Space Grotesk (bold, geometric)
- **Body**: Inter (neutral, legible)

### Responsividad
- Diseño mobile-first
- Breakpoints: 1280px (desktop), 720px (tablet)
- Grid automático que se adapta al ancho de pantalla

## 📈 Funcionalidades Implementadas (Checklist)

### Requerimientos Obligatorios
- ✅ **Base de Datos Relacional**: SQLite con 3 tablas principales (Tienda, Juego, Oferta)
- ✅ **Migraciones y Seeders**: Script `seed_data.py` con datos iniciales
- ✅ **Modelado Eloquent-like**: SQLAlchemy ORM con relaciones correctas
- ✅ **Frontend Responsivo**: HTML5 + CSS3 + JavaScript vanilla (sin jQuery)
- ✅ **Motor de Plantillas**: Jinja2 con layouts y componentes modulares
- ✅ **CRUD Completo**: Crear, leer, actualizar, eliminar para Juegos y Ofertas
- ✅ **Validación Robusta**: Pydantic schemas + FormRequest patterns
- ✅ **Dashboard/Reportes**: Métricas clave, gráficos de distribución
- ✅ **API REST Documentada**: Swagger UI en `/docs`

### Funcionalidades Extra (Puntos Bonus)
- ✅ **Integración de API Externa**: Sincronización con CheapShark en tiempo real
- ✅ **Exportación de Datos**: CSV, Excel (con estilos), PDF (con tablas)
- ✅ **Estadísticas Avanzadas**: Cálculo de ahorros, tendencias, rankings
- ✅ **Sincronización Automática**: Script para actualizar ofertas programadamente

## 🔍 Decisiones de Arquitectura

### ¿Por qué Python/FastAPI en lugar de Laravel/PHP?
1. **Performance**: FastAPI es uno de los frameworks web más rápidos en benchmarks
2. **Desarrollo ágil**: Code generation con IA es más efectivo en Python
3. **Prototipado rápido**: Menos boilerplate, más funcionalidad en menos líneas
4. **Type hints**: Python 3.9+ ofrece type safety comparable a TypeScript
5. **Integración con IA**: Mejor soporte en GitHub Copilot y Claude

### ¿Por qué SQLite en lugar de PostgreSQL?
- **Prototipado**: Sin necesidad de servidor de BD externo
- **Deploy simple**: Base de datos es un archivo único
- **Testing**: Fácil crear BDs temporales en RAM

En producción, migrar a PostgreSQL es trivial: solo cambiar `DATABASE_URL` en `app/database.py`.

## 🧪 Testing

El código está diseñado para ser testeable:
- **Services**: Inyección de dependencias (BD) permite mocks fáciles
- **Repositories**: Consultas centralizadas y reutilizables
- **Models**: Validación a nivel de ORM

## 📝 Commits y Control de Versiones

El repositorio incluye commits frecuentes demostrando progreso incremental:
- Commit 1: Estructura base del proyecto
- Commit 2: Implementación de CRUD de Juegos
- Commit 3: Implementación de CRUD de Ofertas
- Commit 4: Dashboard y estadísticas
- Commit 5: Exportación de reportes
- Commit 6: Mejoras UI/UX y validación
- Commit 7: Documentación final

## 🚦 Estado del Proyecto

| Componente | Estado | Notas |
|-----------|--------|-------|
| Arquitectura en capas | ✅ Completo | 4 capas bien definidas |
| Base de datos | ✅ Completo | 3 tablas con relaciones |
| CRUD Juegos | ✅ Completo | Frontend + API |
| CRUD Ofertas | ✅ Completo | Frontend + API |
| Dashboard | ✅ Completo | 4 métricas + gráficos |
| Exportación | ✅ Completo | CSV, Excel, PDF |
| Sincronización API | ✅ Completo | Integración CheapShark |
| Validación | ✅ Completo | Frontend + Backend |
| Documentación | ✅ Completo | README + código comentado |

## 📞 Soporte y Preguntas

En caso de preguntas sobre la arquitectura o el código, consultar los comentarios en los archivos principales:
- `app/main.py`: Punto de entrada y configuración
- `app/database.py`: Conexión y sesión de BD
- `app/models/models.py`: Definición de entidades
- `app/services/`: Lógica de negocio específica
- `app/repositories/`: Acceso a datos
