"""RabbitMQ helper for the Users microservice."""

from __future__ import annotations

import json
import os
from typing import Any, Callable

try:
    import pika
except ImportError as exc:  # pragma: no cover - friendly runtime error
    raise SystemExit("Missing dependency: install pika with `pip install pika`." ) from exc

try:
    from pika.exceptions import AMQPConnectionError
except ImportError:  # pragma: no cover - fallback for older pika layouts
    AMQPConnectionError = Exception

EXCHANGE_NAME = "novalink.events"
ROUTING_KEY_ORDER_CREATED = "pedido.creado"
ROUTING_KEY_INVENTORY_CONFIRMED = "inventario.confirmado"
ROUTING_KEY_USER_UPDATED = "usuario.actualizado"

QUEUE_INVENTORY = "inventario.pedido.creado"
QUEUE_USERS = "usuarios.inventario.confirmado"
QUEUE_NOTIFICATIONS = "notificaciones.usuario.actualizado"

MessageHandler = Callable[[dict[str, Any]], None]


def build_connection_parameters() -> pika.ConnectionParameters:
    broker_url = os.getenv("RABBITMQ_URL")
    if broker_url:
        return pika.URLParameters(broker_url)

    host = os.getenv("RABBITMQ_HOST", "localhost")
    port = int(os.getenv("RABBITMQ_PORT", "5672"))
    vhost = os.getenv("RABBITMQ_VHOST", "/")
    user = os.getenv("RABBITMQ_USER", "guest")
    # Log connection target to help debugging DNS/resolution issues
    print(f"[rabbitmq] connecting to {host}:{port} vhost={vhost} user={user}")
    return pika.ConnectionParameters(
        host=host,
        port=port,
        virtual_host=vhost,
        credentials=pika.PlainCredentials(
            user,
            os.getenv("RABBITMQ_PASSWORD", "guest"),
        ),
    )


def open_channel() -> tuple[pika.BlockingConnection, pika.adapters.blocking_connection.BlockingChannel]:
    try:
        connection = pika.BlockingConnection(build_connection_parameters())
        return connection, connection.channel()
    except AMQPConnectionError as exc:
        raise SystemExit(
            "Could not connect to RabbitMQ. Start the broker first with:\n"
            "  docker compose -f events-broker/docker-compose.yml up -d\n"
            "Or set RABBITMQ_URL to point to a running broker."
        ) from exc


def declare_event_topology(channel: pika.adapters.blocking_connection.BlockingChannel) -> None:
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct", durable=True)


def declare_service_queue(
    channel: pika.adapters.blocking_connection.BlockingChannel,
    queue_name: str,
    routing_key: str,
) -> None:
    declare_event_topology(channel)
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=routing_key)


def publish_event(routing_key: str, payload: dict[str, Any]) -> None:
    connection, channel = open_channel()
    try:
        declare_event_topology(channel)
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,
            ),
        )
    finally:
        connection.close()


def decode_json_message(body: bytes) -> dict[str, Any]:
    return json.loads(body.decode("utf-8"))


def consume_forever(
    queue_name: str,
    routing_key: str,
    handler: MessageHandler,
) -> None:
    connection, channel = open_channel()
    try:
        declare_service_queue(channel, queue_name, routing_key)

        def on_message(
            _channel: pika.adapters.blocking_connection.BlockingChannel,
            method: pika.spec.Basic.Deliver,
            _properties: pika.spec.BasicProperties,
            body: bytes,
        ) -> None:
            payload = decode_json_message(body)
            handler(payload)
            _channel.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=False)
        print(f"[rabbitmq] waiting for {routing_key} on queue {queue_name}")
        channel.start_consuming()
    finally:
        connection.close()


def consume_once(
    queue_name: str,
    routing_key: str,
    handler: MessageHandler,
) -> bool:
    connection, channel = open_channel()
    try:
        declare_service_queue(channel, queue_name, routing_key)
        method, _properties, body = channel.basic_get(queue=queue_name, auto_ack=False)
        if method is None:
            return False

        payload = decode_json_message(body)
        handler(payload)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return True
    finally:
        connection.close()
