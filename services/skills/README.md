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

## Estructura relevante

- `app/main.py` — Entrypoint FastAPI
- `app/persistence/models.py` — Modelo de Skill
- `app/external/seed_skills.py` — Script para poblar skills de ejemplo

## Notas

- Docstrings y comentarios internos en inglés.

**Última actualización:** 2026-05-24
