FROM python:3.10-slim

WORKDIR /app

# Asegurarse de que los print() se vean inmediatamente en los logs de Docker
ENV PYTHONUNBUFFERED=1

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de events-broker (shared y services)
COPY . .

# Variables de entorno por defecto para conectar con los otros contenedores
ENV RABBITMQ_HOST=rabbitmq
ENV REDIS_HOST=redis
