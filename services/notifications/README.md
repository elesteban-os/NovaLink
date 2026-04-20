# Microservicio de Notificaciones

Servicio REST para gestionar notificaciones de la plataforma NovaLink. Permite que otros servicios notifiquen a los usuarios sobre eventos importantes (completación de pedidos, asignación de habilidades, etc.).

## Inicio Rápido

```bash
cd services/notifications
docker-compose up -d
```

API disponible en: `http://localhost:8004`
- Swagger (documentación interactiva): `http://localhost:8004/docs`

---

## Probar con Postman

### Opción 1: Importar OpenAPI automáticamente

1. Abre Postman
2. Click en **Import** (esquina superior izquierda)
3. Selecciona la pestaña **Link**
4. Pega esta URL: `http://localhost:8004/openapi.json`
5. Click en **Import**
6. Postman generará automáticamente todas las requests con los parámetros correctos

### Opción 2: Crear requests manualmente

#### POST /notifications - Crear notificación

1. **Method:** POST
2. **URL:** `http://localhost:8004/notifications`
3. **Headers:** 
   - `Content-Type: application/json`
4. **Body (raw JSON):**
```json
{
  "user_id": 1,
  "order_id": 10,
  "title": "Habilidad adquirida",
  "description": "Has adquirido la habilidad de Empatía"
}
```
5. Click **Send** → Recibirás **201 Created** con la notificación creada

#### GET /users/{user_id}/notifications - Obtener notificaciones

1. **Method:** GET
2. **URL:** `http://localhost:8004/users/1/notifications`
3. Sin headers ni body necesarios
4. Click **Send** → Recibirás **200 OK** con todas las notificaciones del usuario
5. **Con paginación (opcional):**
   - URL: `http://localhost:8004/users/1/notifications?skip=0&limit=5`

#### DELETE /notifications/{notification_id} - Eliminar notificación

1. **Method:** DELETE
2. **URL:** `http://localhost:8004/notifications/1` (reemplaza 1 con el ID a eliminar)
3. Sin headers ni body necesarios
4. Click **Send** → Recibirás **204 No Content** (sin body de respuesta)

---

## Endpoints

### POST /notifications
Crea una nueva notificación y simula envío de email.

**Que hace:** Almacena la notificación en PostgreSQL e imprime un mensaje formateado en la consola del servidor.

**Para qué:** Permite que servicios externos (Pedidos, Usuarios, Habilidades) notifiquen a los usuarios.

Respuesta (201):
```json
{
  "id": 1,
  "user_id": 1,
  "order_id": 10,
  "title": "Habilidad adquirida",
  "description": "Has adquirido la habilidad de Empatía",
  "created_at": "2026-04-20T10:30:00"
}
```

---

### GET /users/{user_id}/notifications
Obtiene todas las notificaciones de un usuario.

**Que hace:** Recupera el historial de notificaciones del usuario. Por defecto devuelve todas las notificaciones ordenadas por más recientes primero. Soporta paginación opcional mediante parámetros `skip` y `limit`.

**Para qué:** Mostrar el centro de notificaciones en la interfaz de usuario.

Respuesta (200):
```json
{
  "total": 2,
  "count": 2,
  "notifications": [
    {
      "id": 1,
      "user_id": 1,
      "order_id": 10,
      "title": "Habilidad adquirida",
      "description": "Has adquirido la habilidad de Empatía",
      "created_at": "2026-04-20T10:30:00"
    }
  ]
}
```

---

### DELETE /notifications/{notification_id}
Elimina una notificación.

**Que hace:** Elimina permanentemente una notificación del sistema.

**Para qué:** Permitir que usuarios limpien su historial.

Respuesta (204 No Content)

---

## Validaciones

| Campo | Restricción |
|-------|-------------|
| user_id | Debe ser > 0 |
| order_id | Debe ser > 0 |
| title | 1-255 caracteres, no solo espacios |
| description | Mínimo 1 carácter, no solo espacios |

---

## Simulación de Email

Cuando se crea una notificación (POST), el servidor imprime en consola:

```
╔════════════════════════════════════════════════════════════╗
║                    NOTIFICACION DE CORREO                  ║
╚════════════════════════════════════════════════════════════╝

FECHA DE ENVIO: 2026-04-20 15:30:45
NOTIFICATION ID: 1
USER ID: 1
ORDER ID: 10

ASUNTO: Habilidad adquirida

CONTENIDO:
────────────────────────────────────────────────────────────
Has adquirido la habilidad de Empatía
────────────────────────────────────────────────────────────

ESTADO: ENVIADO (SIMULADO)
```

Ver logs: `docker-compose logs -f notifications_api`

---

## Códigos HTTP

| Código | Significado |
|--------|-------------|
| 201 | Notificación creada exitosamente |
| 200 | Solicitud procesada correctamente |
| 204 | Eliminación exitosa |
| 400 | Parámetros inválidos |
| 404 | Notificación no encontrada |
| 422 | Datos no validan esquema |

---

## Variables de Entorno

```
DB_USER=novalink_user
DB_PASSWORD=novalink_password
DB_HOST=postgres_notifications
DB_PORT=5432
DB_NAME=notifications_db
DB_ECHO=false
```

---

## Arquitectura

**main.py** - Endpoints FastAPI
**models.py** - Modelo SQLAlchemy (tabla `notifications`)
**schemas.py** - Esquemas Pydantic para validación
**database.py** - Conexión PostgreSQL
**email_service.py** - Simulación de envío de email

---

## Tecnologías

- FastAPI 0.104.1
- PostgreSQL 15
- SQLAlchemy 2.0.23
- Pydantic 2.5.0
- Docker & docker-compose
