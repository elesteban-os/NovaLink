# RabbitMQ Broker State — NovaLink

## Estado actual

- El broker usado es RabbitMQ con la biblioteca `pika`.
- La topología se define como un exchange directo duradero llamado `novalink.events`.
- Cada consumidor declara su propia cola duradera y la enlaza al exchange con una clave de enrutamiento específica.
- Los mensajes se publican con `delivery_mode=2`, lo que indica que son persistentes.
- Los consumidores usan `basic_ack` después de procesar un mensaje.
- El broker retiene los mensajes mientras exista la cola duradera y el mensaje sea persistente.

## Cómo funciona actualmente

### Topología principal

- Exchange: `novalink.events` (tipo `direct`, durable)
- Colas y claves de enrutamiento:
  - `inventario.pedido.creado` vinculado a `pedido.creado` (consumidor: skills)
  - `usuarios.inventario.confirmado` vinculado a `inventario.confirmado` (consumidor: users)
  - `orders.inventario.sin_stock` vinculado a `inventario.sin_stock` (consumidor: orders)
  - `notificaciones.usuario.actualizado` vinculado a `usuario.actualizado` (consumidor: notifications)

### Flujo de eventos en el ejemplo

**Caso exitoso (stock disponible):**
1. `orders` publica un evento `pedido.creado`.
2. `skills` consume `pedido.creado` desde la cola `inventario.pedido.creado`.
3. `skills` valida stock:
   - ✅ Si hay stock: publica `inventario.confirmado`.
   - ❌ Si no hay stock: publica `inventario.sin_stock`.
4. **Rama exitosa**: `users` consume `inventario.confirmado` desde la cola `usuarios.inventario.confirmado`.
5. `users` asigna habilidad al usuario y publica `usuario.actualizado`.
6. `notifications` consume `usuario.actualizado` desde la cola `notificaciones.usuario.actualizado` y crea notificación.

**Rama de fallo (sin stock):**
4. `orders` consume `inventario.sin_stock` desde la cola `orders.inventario.sin_stock` (solo logs).

### Comportamiento de los auxiliares RabbitMQ

Los archivos de helper (`notify`, `users`, `skills`, `orders`) comparten la misma lógica básica:

- `build_connection_parameters()` lee `RABBITMQ_URL` o `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_VHOST`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`.
- `open_channel()` crea la conexión y canal de RabbitMQ.
- `declare_event_topology()` crea el exchange duradero.
- `declare_service_queue()` declara la cola duradera y la enlaza al exchange.
- `publish_event()` publica JSON al exchange con `content_type=application/json` y `delivery_mode=2`.
- `consume_forever()` inicia `basic_consume` con `auto_ack=False`, `basic_qos(prefetch_count=1)` y `basic_ack` manual.
- `consume_once()` toma un solo mensaje con `basic_get` y lo ackea si fue procesado.

### Mensajes y servicios consumidores

- `services/skills/app/infrastructure/event_worker.py` consume `pedido.creado` y publica `inventario.confirmado` o `inventario.sin_stock` según validación de stock.
- `services/users/app/infrastructure/event_worker.py` consume `inventario.confirmado` y publica `usuario.actualizado`.
- `services/orders/app/infrastructure/event_worker.py` consume `inventario.sin_stock` con fines de auditoría/logs.
- `services/notifications/app/infrastructure/event_worker.py` consume `usuario.actualizado` y crea una notificación en la base de datos.
- El service de notificaciones no publica eventos posteriores; es un consumidor final de este flujo.

## Estado de persistencia

### Qué persiste

- Exchange duradero: la definición del exchange sobrevive a reinicios de broker.
- Colas duraderas: la cola permanece entre reinicios si el broker la guarda.
- Mensajes persistentes: la bandera `delivery_mode=2` solicita que RabbitMQ escriba el mensaje en disco.

### Qué no persiste aquí

- No hay persistencia adicional fuera de RabbitMQ para los mensajes.
- No hay dead-letter queue configurada.
- No hay reintentos automáticos ni política de backoff en el consumidor.
- La fiabilidad depende de la configuración del broker y del estado de las colas.

## Logging y observabilidad actuales

- Se usan impresiones en consola (`print(...)`) en los helpers y workers.
- No hay logging estructurado ni integración con un sistema de logs central.
- El estado esperado se observa vía salida estándar de los servicios:
  - `published` en los servicios que emiten eventos
  - `waiting for ...` en los consumidores
  - `received ...` y `created notification ...` en notificaciones

## Qué falta por mejorar

### Robustez de broker/eventos

- Añadir dead-letter exchanges/colas para mensajes no procesables.
- Implementar reintentos con límite de fallos y backoff.
- Manejar reconexiones automáticamente cuando RabbitMQ no está disponible.
- Añadir timeouts y detección de mensajes huérfanos.

### Observabilidad y monitoreo

- Cambiar `print()` a logger estructurado (`logging` o similar).
- Añadir métricas de mensajes procesados, errores de consumo y tiempos de latencia.
- Registrar eventos de reconexión y fallos en publicación/consumo.

### Validación y seguridad

- Validar el esquema de carga útil antes de procesar en cada handler.
- Manejar valores faltantes / tipos incorrectos de forma explícita.
- Evitar que un mensaje malo derribe el consumidor.

### Cobertura de eventos/endpoints

- El flujo actual implementa un pipeline bidireccional de eventos:
  - **Rama exitosa**: `pedido.creado` → `inventario.confirmado` → `usuario.actualizado` → notificación persisten
  - **Rama de fallo**: `pedido.creado` → `inventario.sin_stock` → logs en orders
- `services/orders` publica `pedido.creado` desde lógica HTTP POST `/orders`.
- `services/orders` consume `inventario.sin_stock` como proceso separado (`event_worker.py`).
- `services/notifications` expone endpoint `POST /notifications` para notificaciones directas (sin broker).
- Los servicios consumen eventos en procesos separados (`event_worker.py`), no como parte de los endpoints HTTP.

## Recomendaciones inmediatas

1. Documentar el flujo de mensajes en un diagrama simple para reconciliar `events-broker/services/*` con `services/*`.
2. Implementar logging estructurado y errores de reconexión en los helpers RabbitMQ.
3. Añadir pruebas de integración que levanten RabbitMQ y verifiquen el paso de evento a evento hasta notificación.
4. Añadir DLQ / reintentos para que fallos de creación de notificación no pierdan mensajes.
