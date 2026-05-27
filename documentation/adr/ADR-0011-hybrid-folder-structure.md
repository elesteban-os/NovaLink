# ADR-0011: Estructura de código híbrida en repositorio único

- Status: Accepted

## Context

Históricamente el proyecto incorporó frontend, backend y, recientemente, contenedores infraestructurales y de mensajería asíncrona (broker). Al separar los dominios en microservicios reales se discutió cómo ordenar el repositorio sin tener que saltar entre de 3 o 4 repos separados.

## Decision

Mantener un repositorio tipo monorepo bajo una arquitectura de carpetas híbrida dividida estrictamente por roles de sistema:
- `services/`: Carpeta puramente contenedora de los backends de dominio (`auth`, `users`, `skills`, `orders`, `notifications`). Aquí residen los microservicios core.
- `events-broker/`: Centraliza el ecosistema de comunicación asíncrona; almacena dependencias de base, configuraciones Docker conjuntas, y los conectores compartidos de Python (`rabbitmq_api.py`, `redis_api.py`).
- `admin-frontend/`: App cliente consumidora frontal y web assets.
- `k8s/` y `documentation/`: Recursos estáticos de operaciones y especificaciones OpenAPI, ADRs.

## Consequences

- **Positivo:** Evita el desacoplamiento de versiones del código para facilitar la orquestación local con Docker Compose en una sola terminal.
- **Positivo:** Todo el código auxiliar del broker está acorralado sin mezclarse en la lógica pura de negocio de las carpetas de servicios.
- **Negativo:** En etapas de CI/CD hay que ser cuidadosos y parsear solo los directorios cambiados (`paths` match) para no hacer builds íntegros por un cambio minúsculo en un solo servicio o simple modificación del front.