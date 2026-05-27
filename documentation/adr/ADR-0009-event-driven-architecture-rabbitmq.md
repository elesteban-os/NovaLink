# ADR-0009: Arquitectura Orientada a Eventos (EDA) con RabbitMQ

- Status: Accepted

## Context

A medida que el número de microservicios crece, la comunicación síncrona vía HTTP entre ellos acopla los servicios fuertemente y reduce la disponibilidad global (si un servicio cae, el flujo HTTP completo falla).
Necesitábamos un mecanismo asíncrono y transparente para notificar cambios de estado (por ejemplo, notificar a `users` y `notifications` cuando desde `orders` o `skills` se afecta el inventario de un perfil).

## Decision

Adoptar una Arquitectura Orientada a Eventos (EDA) para la comunicación inter-servicios utilizando RabbitMQ como Message Broker principal.
- Empleamos un exchange directo duradero llamado `novalink.events`.
- Cada servicio consumidor declara su propia cola y la enlaza al exchange mediante claves de enrutamiento (routing keys) de dominio específicas.
- Los mensajes se publican con persistencia (`delivery_mode=2`), y retención duradera.
- La confirmación se hace de forma manual y explícita (`basic_ack`) desde los consumers.

## Consequences

- **Positivo:** Fuerte desacoplamiento temporal; si un servicio consumidor está temporalmente caído, RabbitMQ acumulará el mensaje hasta que se recupere.
- **Positivo:** Facilidad para incluir nuevos consumidores (extensibilidad).
- **Negativo:** Mayor complejidad de operación e infra al necesitar mantener un clúster de RabbitMQ sano, y se incrementa la dificultad para rastrear transacciones distribuidas completas.