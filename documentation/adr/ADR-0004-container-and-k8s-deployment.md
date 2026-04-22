# ADR-0004: Contenerizacion y despliegue en Kubernetes local

- Status: Accepted

## Context

El proyecto se ejecuta en ambiente local con Docker y Kubernetes (Docker Desktop). Se necesita un camino simple para desarrollo y pruebas integradas.

## Decision

Mantener doble estrategia:
- docker-compose por servicio para desarrollo aislado rapido.
- Manifiestos Kubernetes en k8s/ para integracion del sistema completo.

En Kubernetes:
- Cada API y cada DB se despliega con su Deployment.
- Se exponen APIs por Services tipo LoadBalancer en puertos de desarrollo.
- Se usan PVC para persistencia de PostgreSQL.

