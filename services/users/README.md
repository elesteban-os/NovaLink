# Users Microservice

Servicio FastAPI para gestión de usuarios y sus skills.

API disponible en: `http://localhost:8001`

## Inicio rápido

```bash
cd services/users
docker-compose up -d
```

## Endpoints principales

- `POST /users` — Crear usuario.
- `GET /users` — Listar usuarios.
- `GET /users/{id}` — Obtener usuario por ID.
- `PUT /users/{id}` — Actualizar usuario.
- `DELETE /users/{id}` — Desactivar usuario.
- `POST /users/{id}/skills` — Agregar skill a usuario.
- `GET /users/{id}/skills` — Listar skills de usuario.

## Variables de entorno

```env
DB_USER=novalink_user
DB_PASSWORD=novalink_password
DB_HOST=postgres_users
DB_PORT=5432
DB_NAME=users_db
DB_ECHO=false
SERVER_HOST=0.0.0.0
SERVER_PORT=8001
```

## Estructura relevante

- `app/main.py` — Entrypoint FastAPI
- `app/handlers/users.py` — Routers y endpoints
- `app/services/user_service.py` — Lógica de negocio
- `app/persistence/*` — Modelos, esquemas y CRUD

## Notas

- Los comentarios del código deben estar en inglés según la guía de estilo.

**Última actualización:** 2026-05-24
