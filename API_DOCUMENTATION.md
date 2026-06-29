# Documentación de API REST - SebaStore

## Descripción General

La API REST de SebaStore proporciona acceso programático a todas las funcionalidades del sistema. Está completamente documentada con Swagger UI en `/docs`.

## Autenticación

### Tokens JWT

Los endpoints protegidos requieren autenticación mediante JWT tokens:

1. **Login**: POST `/login` con credenciales
2. **Registro**: POST `/registro` con datos de usuario nuevo
3. El servidor devuelve una cookie con el token válido por 24 horas

### Headers Requeridos

```
Cookie: token=eyJ0eXAiOiJKV1QiLCJhbGc...
```

## Endpoints Principales

### Autenticación (`/`)

#### POST /login
Autenticarse con credenciales

**Request:**
```json
{
  "nombre_usuario": "admin",
  "contraseña": "admin123"
}
```

**Response:**
```
Set-Cookie: token=eyJ0eXAiOiJKV1QiLCJhbGc...; Max-Age=86400
Location: /
```

#### POST /registro
Registrar nuevo usuario

**Request:**
```json
{
  "nombre_usuario": "nuevouser",
  "email": "usuario@ejemplo.com",
  "contraseña": "contraseña123",
  "confirmar_contraseña": "contraseña123"
}
```

#### GET /logout
Cerrar sesión (elimina cookie)

---

### Usuarios (`/api/usuarios/`)

#### GET /api/usuarios/
**Permisos:** Solo administradores

Listar todos los usuarios registrados

**Response:**
```json
[
  {
    "id": 1,
    "nombre_usuario": "admin",
    "email": "admin@sebastore.local",
    "rol": "admin",
    "activo": true
  }
]
```

#### GET /api/usuarios/me
**Permisos:** Autenticado

Obtener perfil del usuario autenticado

#### GET /api/usuarios/{usuario_id}
**Permisos:** Autenticado (puede ver su propio perfil o ser admin)

Obtener datos de un usuario específico

---

### Juegos (`/api/juegos/`)

#### GET /api/juegos/
Listar todos los juegos

**Query Parameters:**
- `limite`: Número máximo de resultados (default: 50)
- `buscar`: Filtro por título
- `offset`: Para paginación

**Response:**
```json
[
  {
    "id": 1,
    "titulo": "Hollow Knight",
    "imagen_url": "https://...",
    "metacritic_score": 90
  }
]
```

#### POST /api/juegos/
**Permisos:** Solo administradores

Crear nuevo juego

#### GET /api/juegos/{juego_id}
Obtener detalles de un juego

#### PUT /api/juegos/{juego_id}
**Permisos:** Solo administradores

Actualizar juego

#### DELETE /api/juegos/{juego_id}
**Permisos:** Solo administradores

Eliminar juego

---

### Ofertas (`/api/ofertas/`)

#### GET /api/ofertas/
Listar ofertas activas

**Query Parameters:**
- `limite`: Número máximo (default: 50)
- `juego_id`: Filtrar por juego
- `tienda_id`: Filtrar por tienda
- `orden`: "descuento", "precio", "rating"

#### POST /api/ofertas/
**Permisos:** Solo administradores

Crear nueva oferta

#### GET /api/ofertas/{oferta_id}
Obtener detalles de una oferta

#### PUT /api/ofertas/{oferta_id}
**Permisos:** Solo administradores

Actualizar oferta

#### DELETE /api/ofertas/{oferta_id}
**Permisos:** Solo administradores

Eliminar oferta

---

### Sincronización (`/api/sync/`)

#### POST /api/sync/cheapshark
Sincronizar ofertas con CheapShark API

**Query Parameters:**
- `paginas`: Número de páginas a sincronizar (default: 1)

**Response:**
```json
{
  "tiendas_creadas": 5,
  "tiendas_actualizadas": 10,
  "juegos_creados": 50,
  "juegos_actualizados": 30,
  "ofertas_nuevas": 120,
  "ofertas_actualizadas": 80
}
```

---

### Exportación (`/api/export/`)

#### GET /api/export/csv
Descargar ofertas como CSV

**Response:** Archivo CSV

#### GET /api/export/excel
Descargar ofertas como Excel

**Response:** Archivo XLSX

#### GET /api/export/pdf
Descargar ofertas como PDF

**Response:** Archivo PDF

---

## Códigos de Estado HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Requiere autenticación |
| 403 | Forbidden - Permiso denegado |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

## Ejemplos de Uso

### Usando cURL

```bash
# Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "nombre_usuario=admin&contraseña=admin123" \
  -c cookies.txt

# Listar juegos
curl http://localhost:8000/api/juegos/ \
  -b cookies.txt

# Crear oferta
curl -X POST http://localhost:8000/api/ofertas/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "juego_id": 1,
    "tienda_id": 1,
    "precio_normal": 59.99,
    "precio_oferta": 29.99,
    "porcentaje_descuento": 50
  }'
```

### Usando Python

```python
import requests

# Session mantiene cookies automáticamente
session = requests.Session()

# Login
session.post('http://localhost:8000/login', data={
    'nombre_usuario': 'admin',
    'contraseña': 'admin123'
})

# Listar juegos
response = session.get('http://localhost:8000/api/juegos/')
juegos = response.json()
print(juegos)

# Crear oferta
response = session.post('http://localhost:8000/api/ofertas/', json={
    'juego_id': 1,
    'tienda_id': 1,
    'precio_normal': 59.99,
    'precio_oferta': 29.99,
    'porcentaje_descuento': 50
})
print(response.json())
```

### Usando JavaScript/Fetch

```javascript
// Login
const loginRes = await fetch('http://localhost:8000/login', {
  method: 'POST',
  credentials: 'include',
  body: new FormData(loginForm)
});

// Listar juegos
const juegosRes = await fetch('http://localhost:8000/api/juegos/', {
  credentials: 'include'
});
const juegos = await juegosRes.json();
console.log(juegos);

// Crear oferta
const ofertaRes = await fetch('http://localhost:8000/api/ofertas/', {
  method: 'POST',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    juego_id: 1,
    tienda_id: 1,
    precio_normal: 59.99,
    precio_oferta: 29.99,
    porcentaje_descuento: 50
  })
});
const oferta = await ofertaRes.json();
console.log(oferta);
```

## Rate Limiting

Por ahora no hay límite de solicitudes. En producción se implementará rate limiting por IP.

## CORS

CORS está habilitado para desarrollo. En producción, restringir a dominios permitidos.

## Versionado

La API está en versión 1.0.0. Los cambios futuros pueden requerir migración de clientes.
