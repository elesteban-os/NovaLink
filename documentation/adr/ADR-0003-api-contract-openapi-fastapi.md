# ADR-0003: Contrato API con FastAPI y OpenAPI

- Status: Accepted

## Context

Los servicios backend exponen REST APIs y el proyecto necesita documentacion clara para consumo, pruebas y mantenimiento.

## Decision

Estandarizar APIs con FastAPI, usando:
- Validacion de payloads con Pydantic.
- Documentacion OpenAPI automatica en /docs y /openapi.json.
- Declaracion explicita de respuestas de error en endpoints criticos.


