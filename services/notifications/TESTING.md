# Pruebas para el servicio `notifications`

## Propósito
Guía completa para ejecutar los tests del servicio `notifications` con Python 3.11, incluyendo la creación del entorno virtual, instalación de dependencias y ejecución desde cero.

## Requisitos previos
- Python 3.11 instalado en el sistema
- Docker y Docker Compose funcionando
- PostgreSQL levantado en Docker vía `docker compose`

## Estructura de tests
- `tests/conftest.py` → Fixtures de base de datos y cliente FastAPI.
- `tests/test_handlers.py` → Pruebas de endpoints HTTP.
- `tests/test_services.py` → Pruebas de la lógica de negocio.
- `tests/test_persistence.py` → Pruebas de acceso a datos con PostgreSQL.
- `tests/test_email_service.py` → Pruebas de la simulación de envío de email.
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

## Levantar los servicios necesarios

Usa Docker Compose desde `services/notifications`:

```powershell
cd services/notifications
docker compose up -d
```

Verifica que los contenedores estén corriendo:

```powershell
docker compose ps
```

El servicio de PostgreSQL estará disponible en `localhost:5432`.

## Ejecutar los tests

### Opción 1: Con entorno activado

```powershell
cd services/notifications
.venv\Scripts\Activate.ps1
pytest tests/ -q
```

### Opción 2: Sin activar el entorno virtual

```powershell
cd services/notifications
.venv\Scripts\python.exe -m pytest tests/ -q
```

### Opción 3: Ejecutar archivos individuales

```powershell
.venv\Scripts\python.exe -m pytest tests/test_handlers.py tests/test_services.py tests/test_email_service.py tests/test_persistence.py -q
```

## Qué verifica cada archivo

- `test_handlers.py`: crea una notificación mediante endpoints HTTP y verifica la validación de payload.
- `test_services.py`: comprueba la lógica de `create_notification` y la llamada a la función de envío de email simulado.
- `test_email_service.py`: valida el retorno de la simulación de envío de email.
- `test_persistence.py`: valida el CRUD real en la tabla `notifications` de PostgreSQL.
- `test_utils.py`: funciones auxiliares de logging y assertions usadas en los tests.

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
.venv\Scripts\python.exe -m pytest tests/ -q
```

## Uso posterior (después del setup inicial)

```powershell
cd services/notifications
docker compose up -d
.venv\Scripts\python.exe -m pytest tests/ -q
```

## Solución de problemas

### Dependencias faltantes o módulo no encontrado
Asegúrate de usar el entorno virtual del servicio y haber instalado las dependencias correctamente:

```powershell
.venv\Scripts\Activate.ps1
.venv\Scripts\python.exe -m pip install -r requirements.txt pytest pytest-asyncio pytest-cov httpx PyJWT
```

### PostgreSQL no accesible
Verifica que Docker esté corriendo y los contenedores estén activos:

```powershell
docker compose ps
```

### Limpiar y reiniciar

```powershell
Remove-Item -Recurse -Force .venv
docker compose down -v
```

Luego repite el pipeline completo.
