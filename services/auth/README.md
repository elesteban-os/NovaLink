# Auth Microservice

Servicio FastAPI encargado de la autenticación y emisión de tokens JWT.

API disponible en: `http://localhost:8007`

## Inicio rápido

```bash
cd services/auth
docker-compose up -d
```

## Endpoints principales

- `POST /auth/login` — Autentica credenciales y devuelve un JWT (`access_token`).
- `GET /health` — Estado de salud del servicio.

## Variables de entorno

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres_auth
DB_PORT=5432
DB_NAME=auth_db
DB_ECHO=false
JWT_SECRET=supersecret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
SERVER_HOST=0.0.0.0
SERVER_PORT=8007
```

## Estructura relevante

- `app/main.py` — Entrypoint FastAPI
- `app/services/auth_service.py` — Lógica de negocio de autenticación
- `app/security/auth.py` — Utilities de JWT y hashing
- `app/persistence/*` — Modelos y CRUD

## Notas

- Los docstrings y comentarios internos del código deben estar en inglés.

**Última actualización:** 2026-05-24
