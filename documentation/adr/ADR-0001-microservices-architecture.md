# ADR-0001: Arquitectura de microservicios por dominio

- Status: Accepted

## Context

NovaLink separa funcionalidades en dominios claros: users, skills, orders, notifications y admin-frontend.
Cada dominio tiene su propio servicio, despliegue y ciclo de cambio.

## Decision

Adoptar una arquitectura de microservicios con servicios independientes por dominio:
- users-api
- skills-api
- orders-api
- notifications-api
- admin-frontend


