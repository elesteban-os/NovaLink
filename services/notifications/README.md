# Notifications Microservice

Servicio REST para gestionar notificaciones en NovaLink.

API disponible en: `http://localhost:8004`

## Inicio rápido

```bash
cd services/notifications
docker-compose up -d
```

## Endpoints principales

- `POST /notifications` — Crear notificación y simular envío de email.
- `GET /users/{user_id}/notifications` — Listar notificaciones de un usuario.
- `DELETE /notifications/{notification_id}` — Eliminar una notificación.

## Variables de entorno

```env
DB_USER=novalink_user
DB_PASSWORD=novalink_password
DB_HOST=postgres_notifications
DB_PORT=5432
DB_NAME=notifications_db
DB_ECHO=false
SERVER_HOST=0.0.0.0
SERVER_PORT=8004
```

## Estructura relevante

- `app/main.py` — Entrypoint FastAPI
- `app/handlers` — Routers
- `app/persistence` — Modelos y esquemas
- `app/email_service.py` — Simulación de envío de email

## Notas

- El envío de email en este servicio es simulado: el cuerpo se imprime en consola y se registra en logs para propósitos de desarrollo.

**Última actualización:** 2026-05-24
