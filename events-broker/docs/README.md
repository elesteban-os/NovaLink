# events-broker

Ejemplo mínimo de mensajería con RabbitMQ para NovaLink.

## Funcionamiento

El flujo usa un exchange directo compartido en `shared/rabbitmq_api.py` y tres eventos:

1. `pedido.creado` sale desde el servicio de pedidos.
2. `inventario.confirmado` sale desde el servicio de inventario.
# events-broker

Ejemplo mínimo de mensajería con RabbitMQ para NovaLink.

## Funcionamiento

El flujo usa un exchange directo compartido en `shared/rabbitmq_api.py` y tres eventos:

1. `pedido.creado` sale desde el servicio de pedidos.
2. `inventario.confirmado` sale desde el servicio de inventario.
3. `usuario.actualizado` sale desde el servicio de usuarios.

Cada servicio tiene una tarea simple:

- `orders.py` crea un JSON hardcodeado y lo publica.
- `skills.py` actúa como inventario: consume el pedido, valida stock de forma fija y publica la confirmación.
- `users.py` consume la confirmación, asigna una habilidad fija y publica la actualización del usuario.
- `notifications.py` consume la actualización y escribe el log final.

## Plantilla por servicio

Cada script está organizado para que el equipo identifique rápido tres puntos:

1. Dónde entra el mensaje.
2. Dónde se coloca la lógica de negocio.
3. Dónde sale el mensaje o se escribe la salida final.

### `orders.py`

- Entrada: no consume mensajes; inicia el flujo.
- Lógica de negocio: `build_sample_order`.
- Salida: `publish_sample_order` publica `pedido.creado`.

### `skills.py`

- Entrada: consume `pedido.creado`.
- Lógica de negocio: `validate_stock`.
- Salida: `handle_order_created` publica `inventario.confirmado`.

### `users.py`

- Entrada: consume `inventario.confirmado`.
- Lógica de negocio: `assign_skill`.
- Salida: `handle_inventory_confirmed` publica `usuario.actualizado`.

### `notifications.py`

- Entrada: consume `usuario.actualizado`.
- Lógica de negocio: `log_confirmation`.
- Salida: no publica otro mensaje; solo imprime el log final.

## Cómo extender la plantilla

Si un compañero necesita implementar otro servicio, puede copiar el patrón:

1. Declarar la cola y la routing key del evento que recibe.
2. Crear una función pequeña para la lógica de negocio.
3. En el handler, leer el mensaje, llamar la lógica y publicar o registrar la salida.
4. Mantener el broker centralizado en `shared/rabbitmq_api.py`.

## Uso como API

El módulo `shared/rabbitmq_api.py` está pensado para que otros servicios lo
importen directamente sin copiar la infraestructura de mensajería.

```python
from shared.rabbitmq_api import publish_event, consume_forever
```

Con esto, tus compañeros pueden usar solo las funciones necesarias y dejar la
lógica de negocio en sus propios servicios.

## Archivos

- `shared/rabbitmq_api.py`: API común para conexión, publicación y consumo.
- `services/orders/orders.py`: productor inicial del flujo.
- `services/skills/skills.py`: consumidor y publicador del paso de inventario.
- `services/users/users.py`: consumidor y publicador del paso de usuarios.
- `services/notifications/notifications.py`: consumidor final del flujo.
- `docker-compose.yml`: levanta RabbitMQ localmente.
- `requirements.txt`: dependencia Python mínima.

## Requisitos

- Python 3.10 o superior.
- Docker Desktop o Docker Engine para levantar RabbitMQ.
- `pika` instalado en el entorno Python.

## Instalación

Desde la raíz del repositorio:

```bash
pip install -r events-broker/requirements.txt
```

## Levantar RabbitMQ

```bash
docker compose -f events-broker/docker-compose.yml up -d
```

La interfaz de administración queda en:

http://localhost:15672

Usuario y contraseña por defecto:

- usuario: `guest`
- contraseña: `guest`

## Cómo ejecutar cada servicio

Abre una terminal por consumidor y ejecuta:

```bash
python events-broker/services/skills/skills.py run
python events-broker/services/users/users.py run
python events-broker/services/notifications/notifications.py run
```

Después dispara el evento inicial desde otra terminal:

```bash
python events-broker/services/orders/orders.py publish
```

## Modo de prueba de un solo mensaje

Si no quieres dejar procesos corriendo, puedes usar `once` en los consumidores:

```bash
python events-broker/services/skills/skills.py once
python events-broker/services/users/users.py once
python events-broker/services/notifications/notifications.py once
python events-broker/services/orders/orders.py publish
```

## Secuencia esperada

1. `orders/orders.py` publica `pedido.creado`.
2. `skills/skills.py` recibe el pedido y publica `inventario.confirmado`.
3. `users/users.py` recibe la confirmación y publica `usuario.actualizado`.
4. `notifications/notifications.py` recibe la actualización y muestra el log final.

## Variables de entorno opcionales

- `RABBITMQ_URL`: conexión completa a RabbitMQ.
- `RABBITMQ_HOST`: host del broker si no usas URL.
- `RABBITMQ_PORT`: puerto del broker.
- `RABBITMQ_VHOST`: virtual host.
- `RABBITMQ_USER`: usuario.
- `RABBITMQ_PASSWORD`: contraseña.

## Nota

Si un script no puede conectarse al broker, mostrará un mensaje claro indicando cómo levantar RabbitMQ con Docker Compose.
