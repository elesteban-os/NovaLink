# NovaLink Event Broker Integration Guide

Este documento describe la guía para cambiar la comunicación entre el frontend React (`admin-frontend`) y los servicios backend para que no hagan llamadas HTTP directas, sino que usen un **API Gateway** que traduzca las peticiones en eventos RabbitMQ y devuelva resultados mediante polling.

## Objetivo

- Desacoplar el frontend de los servicios directos.
- Usar un `api-gateway` como traductor HTTP → RabbitMQ.
- Mantener el frontend en React sin llamadas directas a `localhost:8001`, `8002`, `8004` o `8005`.
- Responder al frontend mediante polling de estado.
- Documentar la ruta de cada servicio y sus cambios necesarios.

## Arquitectura general propuesta

1. El frontend envía peticiones a `services/api-gateway`.
2. El API Gateway publica eventos en RabbitMQ.
3. Los event workers de cada servicio consumen los eventos.
4. Los servicios procesan la lógica y publican respuestas para el gateway.
5. El API Gateway guarda la respuesta y el frontend la lee mediante polling.

## Servicios y archivos clave

### 1. API Gateway

**Ruta propuesta:** `services/api-gateway/`

**Archivos clave:**
- `services/api-gateway/app/main.py`
- `services/api-gateway/app/routes.py`
- `services/api-gateway/app/models.py`
- `services/api-gateway/app/infrastructure/rabbitmq.py`
- `services/api-gateway/app/infrastructure/storage.py`
- `services/api-gateway/app/workers/response_consumer.py`
- `services/api-gateway/Dockerfile`
- `services/api-gateway/requirements.txt`
- `services/api-gateway/docker-compose.yml`

**Responsabilidades:**
- Exponer `POST /api/gateway/request` para recibir operaciones del frontend.
- Exponer `GET /api/gateway/result/{request_id}` para polling de resultados.
- Exponer `GET /api/gateway/health` para comprobación.
- Enviar eventos RabbitMQ con `request_id` de correlación.
- Consumir eventos de respuesta `gateway.respuesta.*`.
- Guardar resultados temporales con TTL.

### 2. Servicio Skills

**Ruta relevante actual:** `services/skills/app/infrastructure/event_worker.py`

**Cambios recomendados:**
- Recibir eventos de tipo `pedido.creado`.
- Incluir `request_id` en el payload entrante.
- Procesar la orden de stock en la lógica existente.
- Publicar una respuesta a RabbitMQ al gateway, por ejemplo: `gateway.respuesta.skills`.
- Añadir un handler de lectura para `skills.listar`.
- Publicar los resultados de lectura como `gateway.respuesta.skills.list`.

**Ejemplo de archivo de cambio:**
- `services/skills/app/infrastructure/event_worker.py`

**Notas clave:**
- Si el evento llega con `request_id`, devolverlo en la respuesta.
- Los eventos de stock interno (`inventario.confirmado`, `inventario.sin_stock`) se mantienen para el flujo de pedido.
- La ruta de lectura debe devolver la lista de skills o el error correspondiente.

### 3. Servicio Users

**Ruta relevante actual:** `services/users/app/infrastructure/event_worker.py`

**Cambios recomendados:**
- Recibir eventos `inventario.confirmado` para continuar el flujo de asignación de skills.
- Usar `request_id` para correlacionar la operación.
- Publicar una respuesta de resultado a `gateway.respuesta.users`.
- Crear un worker adicional para lecturas de datos de usuario si se reemplaza `GET /users` o `GET /users/{id}/skills`.
- Recibir eventos `usuarios.listar` y `usuarios.skills.listar` para lecturas asíncronas.
- Publicar los resultados de lectura como `gateway.respuesta.users.list` y `gateway.respuesta.users.skills`.

**Ejemplo de archivo de cambio:**
- `services/users/app/infrastructure/event_worker.py`

**Operaciones posibles:**
- `usuarios.listar` → responder con la lista de usuarios en `gateway.respuesta.users.list`.
- `usuarios.skills.listar` → responder con las habilidades de un usuario en `gateway.respuesta.users.skills`.
- `usuario.creado` → crear usuario y devolver resultado en `gateway.respuesta.users`.
- `inventario.confirmado` → asignar habilidad y publicar estado de usuario.

### 4. Servicio Notifications

**Ruta relevante actual:** `services/users/app/infrastructure/event_worker.py`

**Cambios recomendados:**
- Recibir eventos `inventario.confirmado`.
- Usar `request_id` para correlacionar la operación.
- Publicar una respuesta de resultado a `gateway.respuesta.users`.
- Crear un worker adicional para lecturas de datos de usuario si se reemplaza `GET /users` o `GET /users/{id}/skills`.

**Ejemplo de archivo de cambio:**
- `services/users/app/infrastructure/event_worker.py`

**Operaciones posibles:**
- `usuarios.listar` → responder con la lista de usuarios.
- `usuarios.skills.listar` → responder con habilidades del usuario.
- `usuario.creado` → crear usuario y devolver resultado.

### 4. Servicio Notifications

**Ruta relevante actual:** `services/notifications/app/infrastructure/event_worker.py`

**Cambios recomendados:**
- Recibir eventos `usuario.actualizado`.
- Guardar la notificación en la base de datos.
- Publicar una respuesta de confirmación al gateway si se necesita correlación.
- Añadir soporte para lecturas de notificaciones si más adelante el frontend necesita consultar historial.
- Si se implementa lectura, consumir `notificaciones.listar` y publicar `gateway.respuesta.notifications.list`.
- Mantener el proceso de consumo como worker separado.

**Ejemplo de archivo de cambio:**
- `services/notifications/app/infrastructure/event_worker.py`

**Notas clave:**
- Este servicio puede ser el último paso del flujo asincrónico.
- No necesariamente necesita exponer HTTP propio para esta guía, solo consume eventos.

### 5. Frontend React

**Archivos actuales:**
- `admin-frontend/src/pages/Skills.jsx`
- `admin-frontend/src/pages/Users.jsx`
- `admin-frontend/src/pages/Orders.jsx`

**Nuevo archivo recomendado:**
- `admin-frontend/src/api/eventGatewayClient.js`

**Cambios recomendados:**
- Reemplazar llamadas directas a servicios backend (`localhost:8001`, `8002`, `8004`, `8005`).
- Enviar peticiones al gateway:
  - `POST http://localhost:8000/api/gateway/request`
- Consumir resultados mediante polling:
  - `GET http://localhost:8000/api/gateway/result/{request_id}`
- Mantener la lógica de UI mientras espera respuesta.

## Operaciones mapeadas por evento

| Frontend | Evento RabbitMQ | Servicio consumidor | Respuesta al gateway |
|---|---|---|---|
| `create_order` | `pedido.creado` | Skills | `gateway.respuesta.skills` |
| `read_skills` | `skills.listar` | Skills | `gateway.respuesta.skills.list` |
| `create_user` | `usuario.creado` | Users | `gateway.respuesta.users` |
| `read_users` | `usuarios.listar` | Users | `gateway.respuesta.users.list` |
| `user_skills` | `usuarios.skills.listar` | Users | `gateway.respuesta.users.skills` |
| `notify` | `notificaciones.crear` | Notifications | `gateway.respuesta.notifications` |
| `read_notifications` | `notificaciones.listar` | Notifications | `gateway.respuesta.notifications.list` |

## Flujo de la operación

1. El usuario interactúa en React.
2. El frontend envía `POST /api/gateway/request`.
3. El gateway publica un evento RabbitMQ que incluye `request_id`.
4. El servicio correspondiente consume el evento.
5. El servicio procesa la lógica y publica un evento de respuesta.
6. El gateway consume la respuesta y la almacena.
7. El frontend consulta `GET /api/gateway/result/{request_id}` hasta obtener resultado.

## Checklist de implementación

- [ ] Crear `services/api-gateway`.
- [ ] Definir los endpoints de gateway (`request`, `result`, `health`).
- [ ] Implementar almacenamiento temporal para resultados.
- [ ] Añadir `request_id` en el broker y en los eventos.
- [ ] Modificar `services/skills/app/infrastructure/event_worker.py`.
- [ ] Modificar `services/users/app/infrastructure/event_worker.py`.
- [ ] Modificar `services/notifications/app/infrastructure/event_worker.py`.
- [ ] Crear `admin-frontend/src/api/eventGatewayClient.js`.
- [ ] Actualizar `admin-frontend/src/pages/Skills.jsx`.
- [ ] Actualizar `admin-frontend/src/pages/Users.jsx`.
- [ ] Actualizar `admin-frontend/src/pages/Orders.jsx`.
- [ ] Revisar `events-broker/shared/rabbitmq_api.py` para centralizar routing keys.
- [ ] Probar flujo completo con Docker y RabbitMQ.

## Notas adicionales

- El gateway puede usar Redis, SQLite o memoria local para resultados temporales.
- Se recomienda un TTL de resultados de 5 minutos.
- El polling debe tener timeout y manejo de errores en el frontend.
- Durante la transición, es posible mantener los endpoints HTTP directos como fallback.

## Rutas de documentación relacionadas

- `events-broker/shared/rabbitmq_api.py`
- `services/skills/app/infrastructure/event_worker.py`
- `services/users/app/infrastructure/event_worker.py`
- `services/notifications/app/infrastructure/event_worker.py`
- `admin-frontend/src/pages/Skills.jsx`
- `admin-frontend/src/pages/Users.jsx`
- `admin-frontend/src/pages/Orders.jsx`

---

Esta guía documenta la ruta propuesta para que los archivos JSX y el frontend no se comuniquen directamente con los servicios, sino mediante un event worker centralizado que usa RabbitMQ.
