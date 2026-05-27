"""Event consumer worker for the Notifications microservice."""

from __future__ import annotations

import argparse
import json

from app.database import SessionLocal
from app.persistence.schemas import NotificationCreate
from app.infrastructure.rabbitmq import (
    QUEUE_NOTIFICATIONS,
    ROUTING_KEY_USER_UPDATED,
    consume_forever,
    consume_once,
)
from app.services.notification_service import (
    create_notification as create_notification_service,
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


def handle_user_updated(user_event: dict[str, object]) -> None:
    print(
        f"[notificaciones] received {ROUTING_KEY_USER_UPDATED}: "
        f"{json.dumps(user_event, ensure_ascii=False)}"
    )

    payload = build_notification_payload(user_event)
    with SessionLocal() as db:
        try:
            notification = create_notification_service(db, payload)
            print(f"[notificaciones] created notification id={notification.id}")
        except Exception as exc:
            print(f"[notificaciones] error creating notification: {exc}")


def run_notifications_service(mode: str = "run") -> None:
    if mode == "run":
        consume_forever(
            QUEUE_NOTIFICATIONS, ROUTING_KEY_USER_UPDATED, handle_user_updated
        )
        return

    processed = consume_once(
        QUEUE_NOTIFICATIONS, ROUTING_KEY_USER_UPDATED, handle_user_updated
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
