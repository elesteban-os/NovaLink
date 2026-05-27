# Pruebas para el servicio `skills`

## Propósito
Esta guía documenta cómo preparar el entorno y ejecutar los tests del servicio `skills` usando el mismo método probado en `orders` y `notifications`.

## Requisitos previos
- Python 3.11 instalado.
- Docker y Docker Compose disponibles.
- El repositorio clonado con acceso a `services/skills`.

## Flujo desde cero
1. Navega al directorio del servicio:

```powershell
cd services/skills
```

2. Crea y activa el entorno virtual:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instala dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install -r requirements.txt pytest
```

4. Levanta PostgreSQL con Docker Compose:

```powershell
docker compose up -d
```

5. Ejecuta los tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

> Si `pytest` no está en `PATH`, usa siempre `python -m pytest` o `.\.venv\Scripts\python.exe -m pytest`.

## Variables de entorno recomendadas
```env
DB_USER=novalink_user
DB_PASSWORD=novalink_password
DB_HOST=localhost
DB_PORT=5435
DB_NAME=skills_db
DB_ECHO=false
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

## Qué verifica cada archivo
- `tests/test_handlers.py`: endpoints HTTP de `/skills`, validación de payload y manejo de errores.
- `tests/test_services.py`: lógica de negocio de `SkillService`, duplicados, reserva de stock y seed.
- `tests/test_persistence.py`: CRUD real en la base de datos usando SQLAlchemy.
- `tests/conftest.py`: fixtures para la base de datos de pruebas y el cliente FastAPI.

## Notas
- La base de datos PostgreSQL de pruebas se expone en el host `localhost:5435` según `docker-compose.yml`.
- El fixture `setup_test_database` recrea el esquema de la base de datos al iniciar la sesión de tests.
- No es necesario levantar el servicio FastAPI completo para ejecutar los tests, pero Docker Compose debe proveer PostgreSQL.

## Detener servicios
```powershell
docker compose down
```
