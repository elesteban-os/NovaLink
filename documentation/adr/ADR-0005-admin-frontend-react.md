# ADR-0005: Frontend administrativo con React

- Status: Accepted

## Context

Se requiere una interfaz administrativa para login y gestion de entidades (users, skills, orders). El frontend existente usa React y axios.

## Decision

Mantener un frontend en React (react-scripts) con:
- react-router-dom para navegacion.
- axios para comunicacion con APIs.
- Build estatico servido por Nginx en contenedor.

