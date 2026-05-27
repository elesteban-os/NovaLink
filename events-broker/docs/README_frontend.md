# Probar NovaLink con el Frontend

Este archivo describe los pasos para levantar la aplicación real y probarla desde el `admin-frontend`.

## Requisitos previos

- Docker y Docker Compose instalados.
- La red `novalink_network` debe existir (el broker la crea automáticamente).
- RabbitMQ debe estar levantado con el broker de eventos.
- Los servicios deben usar sus archivos `.env` locales ya configurados.

## 1. Levantar RabbitMQ

Desde la raíz del repositorio NovaLink:

```bash
docker compose -f events-broker/docker-compose.yml up -d
```

Verifica que el broker esté funcionando:

```bash
docker compose -f events-broker/docker-compose.yml ps
```

## 2. Levantar los servicios reales

1. `services/orders`
2. `services/skills`
3. `services/users`
4. `services/notifications`
5. `services/auth`

Cada servicio tiene su propio `docker-compose.yml` y su archivo `.env` en la carpeta correspondiente.

```bash
docker compose -f services/orders/docker-compose.yml up -d
docker compose -f services/skills/docker-compose.yml up -d
docker compose -f services/users/docker-compose.yml up -d
docker compose -f services/notifications/docker-compose.yml up -d
docker compose -f services/auth/docker-compose.yml up -d
```

## 3. Levantar el API Gateway

El frontend debe comunicarse con los servicios a través del API Gateway. El gateway traduce las peticiones HTTP en eventos RabbitMQ y devuelve resultados a través de polling.

Desde `services/api-gateway/` puedes ejecutar el gateway localmente:

```bash
cd services/api-gateway
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

O usando Docker:

```bash
cd services/api-gateway
docker build -t novalink-api-gateway .
docker run --rm --name api-gateway -p 8000:8000 \
  -e RABBITMQ_HOST=localhost \
  -e RABBITMQ_PORT=5672 \
  -e RABBITMQ_USER=guest \
  -e RABBITMQ_PASSWORD=guest \
  novalink-api-gateway
```

Asegúrate de que el gateway esté disponible en `http://localhost:8000`.

## 4. Levantar el frontend

### Opción A: Usar Docker Compose

Desde `admin-frontend/`:

```bash
cd admin-frontend
docker compose up -d --build
```

Accede la app en:

```text
http://localhost:3000
```

### Opción B: Levantar localmente con npm

Desde `admin-frontend/`:

```bash
cd admin-frontend
npm install
npm start
```

Abre el navegador en:

```text
http://localhost:3000
```

## 5. Probar la app

1. Abre `http://localhost:3000/login`.
2. Ingresa cualquier email y contraseña (el frontend demo acepta credenciales libres).
3. Navega a las pestañas de `Users`, `Skills` y `Orders`.
4. Crea una orden o usa el flujo del frontend para verificar que los servicios reales responden.

> El frontend debe usar el API Gateway en `http://localhost:8000/api/gateway` para acceder a `users`, `skills`, `orders` y `notifications`.

## 6. Endpoints relevantes

- Auth: `http://localhost:8007/auth/login`
- API Gateway: `http://localhost:8000/api/gateway`
- Gateway results: `http://localhost:8000/api/gateway/result/{request_id}`
- (Interno) Orders API: `http://localhost:8005/orders`
- (Interno) Skills API: `http://localhost:8000` 
- (Interno) Users API: `http://localhost:8002`
- (Interno) Notifications API: `http://localhost:8004`

> Nota: si alguno de estos servicios no arranca, revisa los logs con `docker compose logs -f <service_name>`.

## 7. Comandos útiles

```bash
docker compose -f services/orders/docker-compose.yml logs -f orders_api

docker compose -f services/skills/docker-compose.yml logs -f skills_api

docker compose -f services/users/docker-compose.yml logs -f users_api

docker compose -f services/notifications/docker-compose.yml logs -f notifications_api

docker compose -f services/auth/docker-compose.yml logs -f auth_api

docker compose -f admin-frontend/docker-compose.yml logs -f admin-frontend
```

## 8. Qué revisar si el frontend no carga datos

- Que RabbitMQ esté disponible en la red `novalink_network`.
- Que los servicios reales estén saludables y corran en sus puertos.
- Que `admin-frontend` esté levantado en `localhost:3000`.
- Que el backend devuelva respuestas 200 en los endpoints de `orders`, `users`, `skills` y `notifications`.

## 9. Apagar todo

```bash
docker compose -f admin-frontend/docker-compose.yml down

docker compose -f services/orders/docker-compose.yml down

docker compose -f services/skills/docker-compose.yml down

docker compose -f services/users/docker-compose.yml down

docker compose -f services/notifications/docker-compose.yml down

docker compose -f services/auth/docker-compose.yml down

docker compose -f events-broker/docker-compose.yml down
```
