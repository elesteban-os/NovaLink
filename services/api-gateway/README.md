# NovaLink API Gateway

API Gateway para NovaLink que convierte peticiones HTTP del frontend en eventos RabbitMQ y permite la consulta de resultados mediante polling.

## Uso

1. Construye la imagen:
   ```bash
   docker build -t novalink-api-gateway .
   ```
2. Ejecuta el servicio:
   ```bash
   docker run --rm -p 8000:8000 \
     -e RABBITMQ_HOST=localhost \
     -e RABBITMQ_PORT=5672 \
     -e RABBITMQ_USER=guest \
     -e RABBITMQ_PASSWORD=guest \
     novalink-api-gateway
   ```
3. Accede a la documentación en `http://localhost:8000/docs`.

## Uso desde el frontend

El `admin-frontend` debe enviar todas las solicitudes de datos al API Gateway en lugar de hacerlo directamente contra `orders`, `skills`, `users` o `notifications`.

- Base URL recomendada: `http://localhost:8000/api/gateway`
- Endpoint de creación de pedidos: `POST /api/gateway/request`
- Endpoint de consulta de resultados: `GET /api/gateway/result/{request_id}`

En el frontend, la variable de entorno debe configurarse como:

```env
REACT_APP_API_URL=http://localhost:8000/api/gateway
```

## Endpoints

- `POST /api/gateway/request`
- `GET /api/gateway/result/{request_id}`
- `GET /health`
