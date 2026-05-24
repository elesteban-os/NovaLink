"""Event consumer worker for the Skills microservice."""

from __future__ import annotations

import argparse
import json
from typing import Any

from app.database import SessionLocal
from app.rabbitmq import (
    QUEUE_INVENTORY,
    ROUTING_KEY_INVENTORY_CONFIRMED,
    ROUTING_KEY_ORDER_CREATED,
    consume_forever,
    consume_once,
    publish_event,
)
from app.services.skill_service import SkillService

service = SkillService()


def build_inventory_confirmation(order: dict[str, Any], success: bool, reason: str | None = None) -> dict[str, Any]:
    return {
        "pedido_id": order["pedido_id"],
        "user_id": order["user_id"],
        "skill_name": order["skill_name"],
        "quantity": order["quantity"],
        "stock_validado": success,
        "inventario_estado": "confirmado" if success else "rechazado",
        "motivo": reason or "",
    }


def handle_order_created(order: dict[str, Any]) -> None:
    print(f"[inventario] received {ROUTING_KEY_ORDER_CREATED}: {json.dumps(order, ensure_ascii=False)}")

    with SessionLocal() as db:
        try:
            service.reserve_stock(db, order["skill_name"], order["quantity"])
            payload = build_inventory_confirmation(order, True)
        except ValueError as exc:
            payload = build_inventory_confirmation(order, False, str(exc))

    publish_event(ROUTING_KEY_INVENTORY_CONFIRMED, payload)
    print(f"[inventario] published {ROUTING_KEY_INVENTORY_CONFIRMED}: {payload}")


def run_inventory_service(mode: str = "run") -> None:
    if mode == "run":
        consume_forever(QUEUE_INVENTORY, ROUTING_KEY_ORDER_CREATED, handle_order_created)
        return

    processed = consume_once(QUEUE_INVENTORY, ROUTING_KEY_ORDER_CREATED, handle_order_created)
    if not processed:
        print(f"[inventario] no messages available in {QUEUE_INVENTORY}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NovaLink inventory worker")
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
    run_inventory_service(args.action)


if __name__ == "__main__":
    main()
