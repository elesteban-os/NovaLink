# ADR-0010: Idempotencia de consumo de eventos utilizando Redis

- Status: Accepted

## Context

Al utilizar RabbitMQ para EDA, la semántica predeterminada ante cortes de red o reinicios de workers suele ser de entrega _"at-least-once"_ (al menos una vez). Esto implica el riesgo de que un worker consuma un mismo evento válido más de una vez.
Para que los servicios (notificaciones, skills, etc.) no generen efectos indeseados repetidos (ej. descontar inventario doblemente), debemos imponer estrategias de procesamiento idempotentes.

## Decision

Utilizar un cluster compartido de Redis (mediante `events-broker/shared/redis_api.py`) para registrar el procesamiento de los eventos.
- Cada mensaje en tránsito incluye un ID de evento único.
- Antes de aplicar el procesamiento, el consumer verifica la existencia de la clave `processed:{service_name}:{event_id}`.
- Una vez procesado, se registra este identificador en Redis con un tiempo de vida (TTL) adecuado (por defecto 24 hrs).

## Consequences

- **Positivo:** Garantiza que si la red falla tras un procesamiento exitoso pero antes del `ack` al broker, la repetición del mensaje será ignorada sin dañar el estado del negocio.
- **Positivo:** Operaciones ultrarrápidas de comprobación sin sobrecargar las bases de PostgreSQL de cada servicio.
- **Negativo:** Representa una pieza más de infraestructura a mantener (el cluster Redis).