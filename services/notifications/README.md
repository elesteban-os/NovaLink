# Microservicio de Notificaciones

Servicio REST para gestionar notificaciones de la plataforma NovaLink. Permite que otros servicios notifiquen a los usuarios sobre eventos importantes (completación de pedidos, asignación de habilidades, etc.).

## Inicio Rápido

```bash
cd services/notifications
docker-compose up -d
```

API disponible en: `http://localhost:8004`
- Swagger: `http://localhost:8004/docs`

**Nota:** Los ejemplos de curl funcionan en Linux/Mac. Para PowerShell (Windows), ver sintaxis específica en cada endpoint.

## Endpoints

### POST /notifications
Crea una nueva notificación y simula envío de email.

**Que hace:** Almacena la notificación en PostgreSQL e imprime un mensaje formateado en la consola del servidor.

**Para qué:** Permite que servicios externos (Pedidos, Usuarios, Habilidades) notifiquen a los usuarios.

**Con curl (Linux/Mac):**
```bash
curl -X POST "http://localhost:8004/notifications" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "order_id": 10,
    "title": "Habilidad adquirida",
    "description": "Has adquirido la habilidad de Empatía"
  }'
```

**Con PowerShell (Windows):**
```powershell
$body = '{"user_id":1,"order_id":10,"title":"Habilidad adquirida","description":"Has adquirido la habilidad de Empatia"}'
Invoke-WebRequest -Uri "http://localhost:8004/notifications" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body `
  -UseBasicParsing | ConvertFrom-Json
```

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

**Que hace:** Recupera el historial de notificaciones del usuario con paginación.

**Para qué:** Mostrar el centro de notificaciones en la interfaz de usuario.

**Con curl (Linux/Mac):**
```bash
curl -X GET "http://localhost:8004/users/1/notifications"
```

**Con PowerShell (Windows):**
```powershell
Invoke-WebRequest -Uri "http://localhost:8004/users/1/notifications" `
  -Method GET `
  -UseBasicParsing | ConvertFrom-Json
```

**Con paginación (opcional):**
```bash
curl -X GET "http://localhost:8004/users/1/notifications?skip=0&limit=5"
```

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

**Con curl (Linux/Mac):**
```bash
curl -X DELETE "http://localhost:8004/notifications/1"
```

**Con PowerShell (Windows):**
```powershell
Invoke-WebRequest -Uri "http://localhost:8004/notifications/1" `
  -Method DELETE `
  -UseBasicParsing
```

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
