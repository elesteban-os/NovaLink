"""Event consumer worker for the Notifications microservice."""

from __future__ import annotations

import argparse
import json
from typing import Any

from app.database import SessionLocal
from app.persistence.schemas import NotificationCreate
from app.infrastructure.rabbitmq import (
    QUEUE_NOTIFICATIONS,
    ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS,
    ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS_LIST,
    ROUTING_KEY_NOTIFY_CREATE,
    ROUTING_KEY_NOTIFICATIONS_LIST,
    ROUTING_KEY_USER_UPDATED,
    consume_forever,
    consume_once,
    publish_event,
)
from app.services.notification_service import (
    create_notification as create_notification_service,
    get_notifications as get_notifications_service,
)


def build_notification_payload(user_event: dict[str, object]) -> NotificationCreate:
    if user_event.get("inventario_confirmado"):
        title = "Pedido confirmado"
        description = (
            f"El pedido {user_event['pedido_id']} fue confirmado y la habilidad "
            f"{user_event['habilidad_asignada']} fue asignada al usuario {user_event['user_id']}"
        )
    else:
        title = "Pedido rechazado"
        description = (
            f"El pedido {user_event['pedido_id']} no pudo ser procesarse: "
            f"{user_event.get('motivo', 'motivo desconocido')}"
        )

    return NotificationCreate(
        user_id=user_event["user_id"],
        order_id=user_event["pedido_id"],
        title=title,
        description=description,
    )


def serialize_notification(notification: Any) -> dict[str, Any]:
    return {key: value for key, value in notification.__dict__.items() if key != "_sa_instance_state"}


def build_gateway_response(request_id: str | None, status: str, payload: dict[str, Any], message: str) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "status": status,
        "message": message,
        "result": payload,
    }


def handle_user_updated(user_event: dict[str, object]) -> None:
    print(
        f"[notificaciones] received {ROUTING_KEY_USER_UPDATED}: "
        f"{json.dumps(user_event, ensure_ascii=False)}"
    )

    request_id = user_event.get("request_id")
    payload = build_notification_payload(user_event)
    with SessionLocal() as db:
        try:
            notification = create_notification_service(db, payload)
            print(f"[notificaciones] created notification id={notification.id}")
            if request_id:
                gateway_payload = build_gateway_response(
                    request_id,
                    "success",
                    serialize_notification(notification),
                    "Notificación creada",
                )
                publish_event(ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS, gateway_payload)
                print(f"[notificaciones] published {ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS}: {gateway_payload}")
        except Exception as exc:
            print(f"[notificaciones] error creating notification: {exc}")
            if request_id:
                gateway_payload = build_gateway_response(
                    request_id,
                    "error",
                    {"error": str(exc)},
                    "Error creando notificación",
                )
                publish_event(ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS, gateway_payload)
                print(f"[notificaciones] published {ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS}: {gateway_payload}")


def handle_notifications_list(event: dict[str, Any]) -> None:
    request_id = event.get("request_id")
    user_id = event.get("user_id")

    print(f"[notificaciones] received {ROUTING_KEY_NOTIFICATIONS_LIST}: {json.dumps(event, ensure_ascii=False)}")

    with SessionLocal() as db:
        notifications = get_notifications_service(db, user_id)
        result = [serialize_notification(notification) for notification in notifications]

    gateway_payload = {
        "request_id": request_id,
        "status": "success",
        "message": "Notificaciones listadas",
        "result": result,
        "count": len(result),
    }
    publish_event(ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS_LIST, gateway_payload)
    print(f"[notificaciones] published {ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS_LIST}: {gateway_payload}")


def handle_notification_create(event: dict[str, Any]) -> None:
    request_id = event.get("request_id")
    notification_payload = {k: v for k, v in event.items() if k != "request_id"}

    print(f"[notificaciones] received {ROUTING_KEY_NOTIFY_CREATE}: {json.dumps(event, ensure_ascii=False)}")

    with SessionLocal() as db:
        try:
            notification = create_notification_service(db, NotificationCreate(**notification_payload))
            gateway_payload = build_gateway_response(
                request_id,
                "success",
                serialize_notification(notification),
                "Notificación creada",
            )
        except Exception as exc:
            gateway_payload = build_gateway_response(
                request_id,
                "error",
                {"error": str(exc)},
                "Error creando notificación",
            )

    if request_id:
        publish_event(ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS, gateway_payload)
        print(f"[notificaciones] published {ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS}: {gateway_payload}")


def handle_event(message: dict[str, Any], routing_key: str) -> None:
    if routing_key == ROUTING_KEY_USER_UPDATED:
        handle_user_updated(message)
    elif routing_key == ROUTING_KEY_NOTIFICATIONS_LIST:
        handle_notifications_list(message)
    elif routing_key == ROUTING_KEY_NOTIFY_CREATE:
        handle_notification_create(message)
    else:
        print(f"[notificaciones] no handler for routing key {routing_key}")


def run_notifications_service(mode: str = "run") -> None:
    if mode == "run":
        consume_forever(
            QUEUE_NOTIFICATIONS,
            [
                ROUTING_KEY_USER_UPDATED,
                ROUTING_KEY_NOTIFICATIONS_LIST,
                ROUTING_KEY_NOTIFY_CREATE,
            ],
            handle_event,
        )
        return

    processed = consume_once(
        QUEUE_NOTIFICATIONS,
        [
            ROUTING_KEY_USER_UPDATED,
            ROUTING_KEY_NOTIFICATIONS_LIST,
            ROUTING_KEY_NOTIFY_CREATE,
        ],
        handle_event,
    )
    if not processed:
        print(f"[notificaciones] no messages available in {QUEUE_NOTIFICATIONS}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NovaLink notifications event worker")
    parser.add_argument(
        "action",
        nargs="?",
        default="run",
        choices=["run", "once"],
        help="Run forever or process one message if available.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run_notifications_service(args.action)


if __name__ == "__main__":
    main()
