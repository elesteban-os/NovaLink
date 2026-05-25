# Notifications Microservice

Servicio REST para gestionar notificaciones en NovaLink.

API disponible en: `http://localhost:8004`

## Inicio rápido

```powershell
cd services/notifications
docker compose up -d
```

## Probar tests desde cero

1. Abrir PowerShell.
2. Navegar al directorio del servicio:

```powershell
cd services/notifications
```

3. Crear el entorno virtual Python 3.11:

```powershell
py -3.11 -m venv .venv
```

4. Activar el entorno virtual:

```powershell
.venv\Scripts\Activate.ps1
```

5. Instalar dependencias:

```powershell
.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.venv\Scripts\python.exe -m pip install -r requirements.txt pytest pytest-asyncio pytest-cov httpx PyJWT
```

6. Levantar la base de datos y el servicio con Docker Compose:

```powershell
docker compose up -d
```

7. Ejecutar los tests:

```powershell
.venv\Scripts\python.exe -m pytest tests/ -q
```

## Endpoints principales

- `POST /notifications` — Crear notificación y simular envío de email.
- `GET /users/{user_id}/notifications` — Listar notificaciones de un usuario.
- `DELETE /notifications/{notification_id}` — Eliminar una notificación.

## Variables de entorno recomendadas

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
- Los tests nuevos cubren validación de payload, lógica de servicio y la simulación de envío de email.

**Última actualización:** 2026-05-25
