# Pruebas para el servicio `notifications`

## Propósito
Guía completa para ejecutar los tests del servicio `notifications` con Python 3.11, incluyendo la activación del entorno virtual y la validación de persistencia real en PostgreSQL.

## Requisitos previos
- Python 3.11 instalado en el sistema
- Docker y Docker Compose funcionando
- PostgreSQL levantado en Docker

## Estructura de tests
- `tests/conftest.py` → Fixtures de base de datos y cliente FastAPI.
- `tests/test_handlers.py` → Pruebas de endpoints HTTP.
- `tests/test_services.py` → Pruebas de la lógica de negocio.
- `tests/test_persistence.py` → Pruebas de acceso a datos con PostgreSQL.
- `tests/test_utils.py` → Utilidades de logging para tests.

## Configuración inicial del entorno virtual

### Paso 1: Crear y activar el entorno virtual (Python 3.11)

```powershell
cd services/notifications
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

> Nota: Después de activar verás `(.venv)` al inicio del prompt.

### Paso 2: Instalar dependencias

```powershell
.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.venv\Scripts\python.exe -m pip install -r requirements.txt pytest pytest-asyncio pytest-cov httpx PyJWT
```

## Levantar PostgreSQL

Usa Docker Compose desde `services/notifications`:

```powershell
cd services/notifications
docker compose up -d
```

Verifica que los contenedores están corriendo:

```powershell
docker compose ps
```

El servicio de PostgreSQL queda expuesto en el host en el puerto `5432`.

## Ejecutar los tests

### Opción 1: Con entorno activado

```powershell
cd services/notifications
.venv\Scripts\Activate.ps1
pytest tests/test_handlers.py tests/test_services.py tests/test_persistence.py tests/test_utils.py -v
```

### Opción 2: Sin activar (ejecución directa)

```powershell
cd services/notifications
.venv\Scripts\python.exe -m pytest tests/test_handlers.py tests/test_services.py tests/test_persistence.py tests/test_utils.py -v
```

### Opción 3: Versión comprimida

```powershell
.venv\Scripts\python.exe -m pytest tests/ -q
```

## Qué verifica cada archivo

- `test_handlers.py`: crea una notificación mediante endpoints HTTP con validación de esquemas Pydantic.
- `test_services.py`: verifica que `create_notification` persiste la notificación y retorna datos correctos.
- `test_persistence.py`: valida en la tabla real `notifications` usando SQLAlchemy.
- `test_utils.py`: proporciona funciones auxiliares para logging y assertions en tests.

## Notas de base de datos

- Usuario: `novalink_user`
- Contraseña: `novalink_password`
- Host de prueba: `localhost`
- Puerto de prueba: `5432`
- Base de datos: `notifications_db`

## Detener servicios

```powershell
docker compose down
```

## Pipeline completo (setup inicial)

Ejecuta esto una sola vez para preparar todo:

```powershell
cd services/notifications
Remove-Item -Recurse -Force .venv
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.venv\Scripts\python.exe -m pip install -r requirements.txt pytest pytest-asyncio pytest-cov httpx PyJWT
docker compose up -d
.venv\Scripts\python.exe -m pytest tests/test_handlers.py tests/test_services.py tests/test_persistence.py tests/test_utils.py -v
```

## Uso posterior (después del setup inicial)

Luego que está todo configurado, simplemente ejecuta:

```powershell
cd services/notifications
docker compose up -d
.venv\Scripts\python.exe -m pytest tests/ -q
```

## Solución de problemas

### Error de codificación en psycopg2
Si ves `UnicodeDecodeError` en psycopg2, asegúrate de estar usando Python 3.11:

```powershell
.venv\Scripts\python.exe --version
```

Este issue está resuelto en 3.11 pero no en 3.12+.

### Base de datos no accesible
Verifica que Docker está corriendo y que los contenedores están activos:

```powershell
docker compose ps
```

### Limpiar y reiniciar

```powershell
Remove-Item -Recurse -Force .venv
docker compose down -v
```

Luego repite el pipeline completo.

### Detener servicios
```bash
docker compose down
```
