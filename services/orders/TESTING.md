# Pruebas para el servicio `orders`

## Propósito
Esta guía documenta cómo ejecutar los tests del servicio `orders` y cómo levantar la base de datos PostgreSQL necesaria para verificar persistencia real.

## Estructura de tests
- `tests/conftest.py` → Fixtures de base de datos y cliente FastAPI.
- `tests/test_handlers.py` → Pruebas de endpoints HTTP.
- `tests/test_services.py` → Pruebas de la lógica de negocio.
- `tests/test_persistence.py` → Pruebas de acceso a datos con PostgreSQL.

## Dependencias de desarrollo
Instala las dependencias de test:

```bash
cd services/orders
pip install -r requirements-dev.txt
```

> Nota: `requirements-dev.txt` incluye `pytest`, `pytest-asyncio`, `pytest-cov`, `httpx` y `PyJWT`.

## Levantar PostgreSQL
Usa Docker Compose desde `services/orders`:

```bash
cd services/orders
docker compose up -d
```

El servicio de PostgreSQL queda expuesto en el host en el puerto `5433`.

## Ejecutar los tests
Desde la raíz del repositorio o desde `services/orders`:

```bash
cd services/orders
pytest -q
```

## Qué verifica cada archivo
- `test_handlers.py`: crea una orden mediante el endpoint `POST /orders` con JWT válido.
- `test_services.py`: verifica que `create_order` persistente la orden y retorna datos correctos.
- `test_persistence.py`: valida en la tabla real `orders` usando SQLAlchemy.

## Notas de base de datos
- Usuario: `novalink_user`
- Contraseña: `novalink_password`
- Host de prueba: `localhost`
- Puerto de prueba: `5433`
- Base de datos: `orders_db`

### Detener servicios
```bash
docker compose down
```
