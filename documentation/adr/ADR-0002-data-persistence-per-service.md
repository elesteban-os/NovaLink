# ADR-0002: Persistencia por servicio con PostgreSQL

- Status: Accepted

## Context

Cada servicio de backend necesita persistir su propio modelo de datos.
El proyecto ya opera con PostgreSQL y SQLAlchemy en los servicios Python.

## Decision

Aplicar el patron "database per service":
- users-api usa su propia base PostgreSQL.
- skills-api usa su propia base PostgreSQL.
- orders-api usa su propia base PostgreSQL.
- notifications-api usa su propia base PostgreSQL.

En Kubernetes se utilizan Deployments de PostgreSQL separados y PVC por dominio.

