# Skills Microservice

Servicio FastAPI que gestiona el catálogo de habilidades y el seeding inicial.

API disponible en: `http://localhost:8006`

## Inicio rápido

```bash
cd services/skills
docker-compose up -d
```

## Endpoints principales

- `GET /skills` — Listar skills disponibles.
- `POST /skills` — Crear una skill (uso interno / administración).
- `GET /health` — Estado de salud del servicio.

## Variables de entorno

```env
DB_USER=novalink_user
DB_PASSWORD=novalink_password
DB_HOST=postgres_skills
DB_PORT=5432
DB_NAME=skills_db
DB_ECHO=false
SERVER_HOST=0.0.0.0
SERVER_PORT=8006
```

## Pruebas

1. Navega al directorio del servicio:

```powershell
cd services/skills
```

2. Crea y activa un entorno virtual con Python 3.11:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instala dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install -r requirements.txt pytest
```

4. Levanta la base de datos PostgreSQL necesaria para los tests:

```powershell
docker compose up -d
```

5. Ejecuta los tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -q
```

> Si `pytest` no se reconoce en la terminal, usa `python -m pytest`.

## Estructura relevante

- `app/main.py` — Entrypoint FastAPI
- `app/persistence/models.py` — Modelo de Skill
- `app/external/seed_skills.py` — Script para poblar skills de ejemplo

## Notas

- Docstrings y comentarios internos en inglés.

**Última actualización:** 2026-05-24
