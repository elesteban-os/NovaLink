# Orders Microservice

Servicio FastAPI que gestiona las órdenes de habilidades en NovaLink.

API disponible en: `http://localhost:8005`

## Inicio rápido

```bash
cd services/orders
docker-compose up -d
```

## Requisitos de Python

Este microservicio debe ejecutarse con Python 3.11.
No uses Python 3.14 directamente porque `pydantic-core` y `psycopg2-binary` pueden fallar en compilación.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
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
