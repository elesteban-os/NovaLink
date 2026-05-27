"""Event consumer worker for the Users microservice."""

from __future__ import annotations

import argparse
import json
from typing import Any

from app.database import SessionLocal
from app.persistence.schemas import UserSkillCreate
from app.infrastructure.rabbitmq import (
    QUEUE_USERS,
    ROUTING_KEY_INVENTORY_CONFIRMED,
    ROUTING_KEY_USER_UPDATED,
    consume_forever,
    consume_once,
    publish_event,
)
from app.services.user_service import user_service
from app.infrastructure.redis import (
    acquire_processing_lock,
    is_event_processed,
    mark_event_processed,
)


def build_user_updated_event(
    inventory_event: dict[str, Any], assigned: bool, reason: str | None = None
) -> dict[str, Any]:
    return {
        "pedido_id": inventory_event["pedido_id"],
        "user_id": inventory_event["user_id"],
        "skill_name": inventory_event["skill_name"],
        "quantity": inventory_event["quantity"],
        "inventario_confirmado": inventory_event["stock_validado"],
        "habilidad_asignada": inventory_event["skill_name"] if assigned else "",
        "usuario_estado": "actualizado" if assigned else "pendiente",
        "motivo": reason or "",
    }


def handle_inventory_confirmed(inventory_event: dict[str, Any]) -> None:
    print(
        f"[usuarios] received {ROUTING_KEY_INVENTORY_CONFIRMED}: "
        f"{json.dumps(inventory_event, ensure_ascii=False)}"
    )
    event_id = inventory_event.get("pedido_id")
    if not event_id:
        print("[usuarios] missing pedido_id in message, skipping idempotency checks")
        return

    if is_event_processed(event_id):
        print(f"[usuarios] already processed {event_id}, skipping")
        return

    if not acquire_processing_lock(event_id, ttl=30):
        print(f"[usuarios] another worker is processing {event_id}, skipping")
        return

    assigned = False
    reason: str | None = None
    if inventory_event.get("stock_validado"):
        with SessionLocal() as db:
            try:
                skill_data = UserSkillCreate(
                    skill_name=inventory_event["skill_name"], points=1
                )
                user_service.add_user_skill(db, inventory_event["user_id"], skill_data)
                assigned = True
            except ValueError as exc:
                reason = str(exc)
    else:
        reason = (
            inventory_event.get("motivo") or "Stock insuficiente o skill no disponible"
        )

    user_update = build_user_updated_event(inventory_event, assigned, reason)
    publish_event(ROUTING_KEY_USER_UPDATED, user_update)
    print(f"[usuarios] published {ROUTING_KEY_USER_UPDATED}: {user_update}")
    mark_event_processed(event_id)


def run_users_service(mode: str = "run") -> None:
    if mode == "run":
        consume_forever(
            QUEUE_USERS, ROUTING_KEY_INVENTORY_CONFIRMED, handle_inventory_confirmed
        )
        return

    processed = consume_once(
        QUEUE_USERS, ROUTING_KEY_INVENTORY_CONFIRMED, handle_inventory_confirmed
    )
    if not processed:
        print(f"[usuarios] no messages available in {QUEUE_USERS}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NovaLink users event worker")
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
    run_users_service(args.action)


if __name__ == "__main__":
    main()
