# Orders Microservice

Servicio FastAPI que gestiona las órdenes de habilidades en NovaLink.

API disponible en: `http://localhost:8005`

## Inicio rápido

```bash
cd services/orders
docker-compose up -d
```

## Endpoints principales

- `POST /orders` — Crear una nueva orden (body: `user_id`, `skill_name`, `quantity`).
- `GET /users/{user_id}/orders` — Listar órdenes de un usuario con paginación (`skip`, `limit`).
- `DELETE /orders/{order_id}` — Eliminar una orden.

## Variables de entorno

```env
DB_USER=novalink_user
DB_PASSWORD=novalink_password
DB_HOST=postgres_orders
DB_PORT=5432
DB_NAME=orders_db
DB_ECHO=false
SERVER_HOST=0.0.0.0
SERVER_PORT=8005
```

## Estructura relevante

- `app/main.py` — Entrypoint FastAPI
- `app/handlers` — Routers y endpoints
- `app/persistence` — Modelos, esquemas y CRUD
- `Dockerfile`, `docker-compose.yml` — Contenerización y orquestación

## Notas

- Validaciones de formato y tipo se realizan con Pydantic. Las comprobaciones de existencia de usuario y disponibilidad de skill son responsabilidad del cliente o de capas superiores antes de crear la orden.

**Última actualización:** 2026-05-24
