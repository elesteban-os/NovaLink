# Pruebas para el servicio `orders`

## Propósito
Esta guía documenta cómo preparar el entorno desde cero y ejecutar los tests del servicio `orders`, incluyendo la validación del JWT real con el servicio `auth` y la base de datos PostgreSQL necesaria para la integración.

## Requisitos previos
- Python 3.11 instalado.
- Docker y Docker Compose disponibles.
- El repositorio clonado con acceso a `services/orders` y `services/auth`.

## Flujo desde cero
1. Abre una terminal y ve a `services/auth`.
2. Levanta el contenedor del servicio de autenticación.
3. En otra terminal, ve a `services/orders`.
4. Levanta el contenedor de PostgreSQL para `orders`.
5. Crea y activa el entorno virtual en `services/orders`.
6. Instala dependencias y ejecuta los tests.

## 1. Levantar el servicio `auth`
Desde la raíz del proyecto o directamente en `services/auth`:

```powershell
cd services/auth
docker compose up -d
```

Esto inicia:
- `postgres_auth` en el contenedor de PostgreSQL para `auth`.
- `auth_api` en `http://localhost:8007`.

El login de prueba esperado es:
- Email: `test@example.com`
- Password: `password123`

Si el contenedor de `auth` se levanta en otro host/puerto, ajusta `AUTH_SERVICE_URL` en la sección de variables de entorno.

## 2. Levantar la base de datos para `orders`
Desde `services/orders`:

```powershell
cd services/orders
docker compose up -d
```

Esto inicia:
- `postgres_orders` con el puerto expuesto `5436:5432`.

Si deseas ejecutar el servicio `orders` dentro de Docker también, `orders_api` quedará disponible en `http://localhost:8005`, pero no es necesario para ejecutar los tests.

## 3. Crear y activar el entorno virtual de `orders`
PowerShell:

```powershell
cd services/orders
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools
pip install -r requirements.txt
```

Bash:

```bash
cd services/orders
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools
pip install -r requirements.txt
```

## 4. Variables de entorno para pruebas
Estas son las variables principales usadas por los tests de `orders`.

PowerShell:

```powershell
$env:DB_HOST = 'localhost'
$env:DB_PORT = '5436'
$env:DB_USER = 'novalink_user'
$env:DB_PASSWORD = 'novalink_password'
$env:DB_NAME = 'orders_db'
$env:AUTH_SERVICE_URL = 'http://localhost:8007/auth/login'
$env:AUTH_TEST_USER_EMAIL = 'test@example.com'
$env:AUTH_TEST_USER_PASSWORD = 'password123'
```

Bash:

```bash
export DB_HOST=localhost
export DB_PORT=5436
export DB_USER=novalink_user
export DB_PASSWORD=novalink_password
export DB_NAME=orders_db
export AUTH_SERVICE_URL=http://localhost:8007/auth/login
export AUTH_TEST_USER_EMAIL=test@example.com
export AUTH_TEST_USER_PASSWORD=password123
```

> Nota: el token JWT real se obtiene desde `auth` usando el endpoint `POST /auth/login`.

## 5. Ejecutar los tests
Desde `services/orders` con el entorno virtual activado:

```powershell
cd services/orders
.\.venv\Scripts\Activate.ps1
pytest -q
```

```bash
cd services/orders
source .venv/bin/activate
pytest -q
```

### Ejecutar sólo tests unitarios
```powershell
cd services/orders
.\.venv\Scripts\Activate.ps1
pytest -q tests/test_services.py tests/test_handlers.py
```

### Ejecutar sólo tests de persistencia
```powershell
cd services/orders
.\.venv\Scripts\Activate.ps1
pytest -q tests/test_persistence.py
```

> Asegúrate de tener el contenedor `postgres_orders` activo antes de correr los tests de persistencia.

## 6. Validación del JWT real de `auth`
Las pruebas que dependen de JWT real usan por defecto:
- `AUTH_SERVICE_URL = http://localhost:8007/auth/login`
- `AUTH_TEST_USER_EMAIL = test@example.com`
- `AUTH_TEST_USER_PASSWORD = password123`

Si `auth` no está disponible, esas pruebas se omiten automáticamente.

## 7. Comando alternativo para todo desde `services/orders`
Si ya tienes los contenedores levantados y el entorno virtual creado, puedes ejecutar:

```powershell
cd services/orders
.\.venv\Scripts\Activate.ps1
python run_tests.py
```

O bien:

```bash
cd services/orders
source .venv/bin/activate
python run_tests.py
```

## Qué verifica cada archivo
- `tests/test_handlers.py` → endpoint `POST /orders` con JWT y validaciones HTTP.
- `tests/test_services.py` → lógica de negocio de creación de órdenes.
- `tests/test_persistence.py` → acceso a datos con PostgreSQL real.

## Detalles de infraestructura
- `services/auth/docker-compose.yml` expone `auth_api` en `8007`.
- `services/orders/docker-compose.yml` expone `postgres_orders` en `5436`.
- El servicio `orders` puede usar `http://localhost:8005` si quieres probar la API en Docker.

## Detener los contenedores
Desde `services/orders`:

```bash
docker compose down
```

Desde `services/auth`:

```bash
cd services/auth
docker compose down
```
