# Microservicio de Órdenes

Servicio FastAPI para gestionar órdenes de habilidades en la plataforma NovaLink. Almacena **solo pedidos exitosos** tras validar que el usuario existe y la habilidad tiene disponibilidad.

## Inicio Rápido

```bash
docker-compose up -d
```

**API**: http://localhost:8005  
**Swagger (Documentación)**: http://localhost:8005/docs  
**OpenAPI JSON**: http://localhost:8005/openapi.json

## Probar con Postman

### Opción 1: Importar OpenAPI Automáticamente

1. Abre Postman
2. Ve a **Import**
3. Selecciona **Link**
4. Pega: `http://localhost:8005/openapi.json`
5. Click en **Import**

Postman importará automáticamente todos los endpoints, esquemas, ejemplos y métodos HTTP.

### Opción 2: Crear Requests Manualmente

#### POST /orders - Crear nueva orden

- **Method**: POST
- **URL**: http://localhost:8005/orders
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Body** (JSON):
  ```json
  {
    "user_id": 1,
    "skill_name": "Liderazgo",
    "quantity": 2
  }
  ```
- **Respuesta esperada** (201 Created):
  ```json
  {
    "id": 1,
    "user_id": 1,
    "skill_name": "Liderazgo",
    "quantity": 2,
    "created_at": "2026-04-20T15:30:00.123456"
  }
  ```

#### GET /users/{user_id}/orders - Listar órdenes del usuario

- **Method**: GET
- **URL**: http://localhost:8005/users/1/orders
- **Headers**: `Content-Type: application/json`
- **Query Params** (opcionales):
  - `skip=0` (default) - Registros a saltar
  - `limit=null` (default) - Máximo de registros (null = todos)
- **Respuesta esperada** (200 OK):
  ```json
  {
    "total": 2,
    "count": 2,
    "orders": [
      {
        "id": 2,
        "user_id": 1,
        "skill_name": "Empatía",
        "quantity": 1,
        "created_at": "2026-04-20T15:35:00.654321"
      },
      {
        "id": 1,
        "user_id": 1,
        "skill_name": "Liderazgo",
        "quantity": 2,
        "created_at": "2026-04-20T15:30:00.123456"
      }
    ]
  }
  ```

#### DELETE /orders/{order_id} - Eliminar orden

- **Method**: DELETE
- **URL**: http://localhost:8005/orders/1
- **Headers**: `Content-Type: application/json`
- **Respuesta esperada** (204 No Content):
  ```
  (vacío)
  ```

## Endpoints

### POST /orders

**Qué hace**: Registra una nueva orden de habilidad. Solo almacena si las validaciones previas (usuario existe, habilidad disponible) fueron exitosas.

**Para qué**: Crear un pedido cuando un usuario quiere adquirir una habilidad.

**Validaciones**:
- `user_id` debe ser > 0 (Pydantic)
- `skill_name` de 1-255 caracteres, no solo espacios (Pydantic)
- `quantity` debe ser > 0 (Pydantic)
- Nota: Validaciones de disponibilidad y usuario válido deben hacerse **antes** de llamar este endpoint

### GET /users/{user_id}/orders

**Qué hace**: Retorna todas las órdenes exitosas de un usuario, ordenadas por más recientes primero.

**Para qué**: Obtener el historial de pedidos completados de un usuario con paginación opcional.

**Parámetros**:
- `user_id` (path, obligatorio) - ID del usuario
- `skip` (query, opcional, default=0) - Registros a saltar
- `limit` (query, opcional, default=null) - Máximo de registros (null devuelve todos)

### DELETE /orders/{order_id}

**Qué hace**: Elimina una orden permanentemente.

**Para qué**: Cancelar o remover un pedido del sistema.

## Validaciones

| Campo | Restricción | Nivel | Error |
|-------|-------------|-------|-------|
| user_id | > 0 | Pydantic | 422 |
| skill_name | 1-255 chars, no espacios | Pydantic | 422 |
| quantity | > 0 | Pydantic | 422 |
| user_id (GET) | > 0 | Lógica | 400 |
| order_id (DELETE) | Debe existir | Lógica | 404 |

**Nota**: Las validaciones de existencia de usuario y disponibilidad de habilidad son responsabilidad del **cliente** antes de llamar POST /orders.

## Códigos HTTP

| Código | Significado | Casos |
|--------|-------------|-------|
| 200 | OK | GET exitoso |
| 201 | Created | POST exitoso (pedido registrado) |
| 204 | No Content | DELETE exitoso |
| 400 | Bad Request | ID de usuario inválido en GET |
| 404 | Not Found | Orden no existe en DELETE |
| 422 | Unprocessable Entity | Validación Pydantic fallida en POST |

## Estructura de Base de Datos

```
Tabla: orders
├── id (Integer, PK, auto-increment)
├── user_id (Integer, FK, NOT NULL, INDEX)
├── skill_name (String(255), FK, NOT NULL, INDEX)
├── quantity (Integer, NOT NULL)
└── created_at (DateTime, auto, NOT NULL)
```

- **order_id**: Identificador único de la orden
- **user_id**: Foreign key a tabla de usuarios
- **skill_name**: Foreign key a tabla de habilidades
- **quantity**: Cantidad solicitada de la habilidad
- **created_at**: Timestamp de creación (server-side)

## Variables de Entorno

```
DB_USER=novalink_user              # Usuario de PostgreSQL
DB_PASSWORD=novalink_password      # Contraseña de PostgreSQL
DB_HOST=postgres_orders            # Host de la BD (servicio Docker)
DB_PORT=5432                       # Puerto de PostgreSQL
DB_NAME=orders_db                  # Nombre de la BD
DB_ECHO=false                      # Mostrar SQL en consola
SERVER_HOST=0.0.0.0                # Host del servidor
SERVER_PORT=8005                   # Puerto del servidor
```

## Arquitectura

### Componentes

- **main.py**: Endpoints FastAPI (POST, GET, DELETE)
- **models.py**: Modelo SQLAlchemy (tabla `orders`)
- **schemas.py**: Esquemas Pydantic para validación
- **database.py**: Configuración de conexión a PostgreSQL
- **Dockerfile**: Imagen Docker con Python 3.11-slim
- **docker-compose.yml**: Orquestación de PostgreSQL + FastAPI

### Flujo de Datos

1. Cliente envía request (JSON)
2. **Pydantic** valida formato y tipos
3. **main.py** valida lógica de negocio
4. **SQLAlchemy** persiste en **PostgreSQL**
5. Respuesta JSON retorna al cliente

## Tecnologías

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| FastAPI | 0.104.1 | Framework REST API |
| SQLAlchemy | 2.0.23 | ORM para PostgreSQL |
| Pydantic | 2.5.0 | Validación de datos |
| PostgreSQL | 15 Alpine | Base de datos relacional |
| Uvicorn | 0.24.0 | Servidor ASGI |
| psycopg2 | 2.9.9 | Driver PostgreSQL |
| python-dotenv | 1.0.0 | Variables de entorno |

## Logs y Debugging

```bash
# Ver logs del servicio
docker-compose logs -f orders_api

# Ver logs de PostgreSQL
docker-compose logs -f postgres_orders

# Ejecutar bash en el contenedor
docker-compose exec orders_api bash
```

## Parar el Servicio

```bash
docker-compose down
```

Para remover volúmenes (borrar BD):
```bash
docker-compose down -v
```

---

**Última actualización**: 2026-04-20  
**Versión del Servicio**: 1.0.0
