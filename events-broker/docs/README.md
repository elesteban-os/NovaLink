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

## Probar con los servicios reales de NovaLink

Para validar el flujo con los servicios reales en `services/*`, sigue estos pasos:

1. Inicia RabbitMQ desde el broker:

```bash
docker compose -f events-broker/docker-compose.yml up -d
```

2. Asegúrate de que la red `novalink_network` exista y sea la misma que usan los servicios reales.
   - El compose del broker ya crea la red con `name: novalink_network`.
   - Los `docker-compose.yml` de `services/users`, `services/skills`, `services/notifications`, `services/orders` están configurados para usar esa red externa.

3. Arranca cada servicio real (API + worker) en su propio compose o sus propios contenedores.
   - En `services/users`: `users_api` y `users_worker`
   - En `services/skills`: `skills_api` y `skills_worker`
   - En `services/notifications`: `notifications_api` y `notifications_worker`
   - En `services/orders`: `orders_api`

4. Verifica que cada servicio vea el broker como `rabbitmq` gracias a la red compartida.

5. Genera un pedido real desde el servicio de órdenes o desde su API, y observa cómo el flujo avanza:
   - `orders` publica `pedido.creado`
   - `skills` consume `pedido.creado` y publica `inventario.confirmado`
   - `users` consume `inventario.confirmado` y publica `usuario.actualizado`
   - `notifications` consume `usuario.actualizado`

### Probar el flujo real con auth y token JWT

1. Levanta RabbitMQ y todos los servicios reales desde la carpeta raíz `NovaLink`:

```bash
# Broker
docker compose -f events-broker/docker-compose.yml up -d

# Servicios reales
docker compose -f services/orders/docker-compose.yml up -d
docker compose -f services/skills/docker-compose.yml up -d
docker compose -f services/users/docker-compose.yml up -d
docker compose -f services/notifications/docker-compose.yml up -d
docker compose -f services/auth/docker-compose.yml up -d
```

> Recomendación: si has cambiado código en un servicio, reconstruye la imagen antes de levantarlo con cache desactivado para asegurarte de usar la versión más reciente.
>
> ```bash
docker compose -f services/orders/docker-compose.yml build --no-cache
docker compose -f services/skills/docker-compose.yml build --no-cache
docker compose -f services/users/docker-compose.yml build --no-cache
docker compose -f services/notifications/docker-compose.yml build --no-cache
docker compose -f services/auth/docker-compose.yml build --no-cache
```
>
> Luego arranca los servicios:
>
> ```bash
docker compose -f services/orders/docker-compose.yml up -d
docker compose -f services/skills/docker-compose.yml up -d
docker compose -f services/users/docker-compose.yml up -d
docker compose -f services/notifications/docker-compose.yml up -d
docker compose -f services/auth/docker-compose.yml up -d
```

2. Obtén el token desde el servicio `auth`:

En PowerShell, ejecuta cada línea por separado:

```powershell
$body = '{"email":"test@example.com","password":"password123"}'
$resp = Invoke-RestMethod -Method Post -Uri 'http://localhost:8007/auth/login' -ContentType 'application/json' -Body $body
$token = $resp.access_token
Write-Output $token
```

3. Crea la orden en el servicio `orders` usando el JWT:

```powershell
$headers = @{'Content-Type'  = 'application/json'; 'Authorization' = "Bearer $token"}
$body = '{"skill_name":"python","quantity":1}'
Invoke-RestMethod -Method Post -Uri 'http://localhost:8005/orders' -Headers $headers -Body $body
```

4. Si prefieres `curl.exe` en PowerShell, usa los siguientes comandos:

```powershell
curl.exe -X POST "http://localhost:8007/auth/login" -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"password123"}'
```

```powershell
curl.exe -X POST "http://localhost:8005/orders" -H "Content-Type: application/json" -H "Authorization: Bearer $token" -d '{"skill_name":"amistad","quantity":1}'
```

Si obtienes 401, verifica que el token se haya copiado completo y que el servicio `auth` está levantado en `http://localhost:8007`.

### Probar el flujo real con una orden

Después de levantar todo, usa otra terminal para llamar al endpoint de órdenes. Si tu servicio requiere token JWT, reemplaza `<JWT_TOKEN>` por uno válido del servicio de auth.

```bash
curl -X POST http://localhost:8005/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -d '{"skill_name":"python","quantity":1,"description":"Prueba de broker"}'
```

Si no usas auth, el endpoint devuelve 401 y debes obtener token desde `auth`.

### Ver logs en terminales separadas
Seb p8eden ver en la aplicación de docker desktop
Si quieres ver la actividad de cada servicio sin `-d`, usa:

```bash
docker compose logs -f users_worker
```

o en la carpeta del servicio correspondiente:

```bash
docker compose logs -f skills_worker
```

### Qué revisar si no funciona

- Levanta RabbitMQ:

```bash
docker compose -f events-broker/docker-compose.yml up -d
```

- Levanta el broker de servicios reales (en cada carpeta de servicio):

```bash
docker compose up -d
```

- Luego envía un pedido real desde `orders` o desde su endpoint REST.

### Qué revisar si no funciona

- Que RabbitMQ esté vivo en `rabbitmq:5672` dentro de los contenedores.
- Que los servicios reales estén unidos a `novalink_network`.
- Que `RABBITMQ_HOST` en los servicios sea `rabbitmq` y no `localhost`.
- Que los workers reales ejecuten `python app/infrastructure/event_worker.py run`.

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
