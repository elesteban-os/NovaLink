# ADR-0008: Configuracion por variables de entorno

- Status: Accepted

## Context

Cada servicio requiere valores de conexion, puertos y flags de ejecucion. El proyecto ya utiliza env vars en compose y manifests.

## Decision

Centralizar configuracion operativa mediante variables de entorno en todos los servicios.

Cobertura minima:
- Credenciales y host de base de datos.
- Puerto y host de servidor.
- URL de conexion completa cuando aplique.
