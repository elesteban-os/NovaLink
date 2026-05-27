"""Event consumer worker for the Skills microservice."""

from __future__ import annotations

import argparse
import json
from typing import Any

from app.database import SessionLocal
from app.infrastructure.rabbitmq import (
    QUEUE_INVENTORY,
    ROUTING_KEY_GATEWAY_RESPONSE_SKILLS,
    ROUTING_KEY_GATEWAY_RESPONSE_SKILLS_LIST,
    ROUTING_KEY_INVENTORY_CONFIRMED,
    ROUTING_KEY_INVENTORY_OUT_OF_STOCK,
    ROUTING_KEY_ORDER_CREATED,
    ROUTING_KEY_SKILLS_LIST,
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


def serialize_skill(skill: Any) -> dict[str, Any]:
    return {key: value for key, value in skill.__dict__.items() if key != "_sa_instance_state"}


def build_gateway_response(request_id: str | None, status: str, payload: dict[str, Any], message: str) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "status": status,
        "message": message,
        "result": payload,
    }


def handle_order_created(order: dict[str, Any]) -> None:
    print(f"[inventario] received {ROUTING_KEY_ORDER_CREATED}: {json.dumps(order, ensure_ascii=False)}")
    request_id = order.get("request_id")

    with SessionLocal() as db:
        try:
            service.reserve_stock(db, order["skill_name"], order["quantity"])
            confirmation = build_inventory_confirmation(order, True)
            publish_event(ROUTING_KEY_INVENTORY_CONFIRMED, confirmation)
            print(f"[inventario] published {ROUTING_KEY_INVENTORY_CONFIRMED}: {confirmation}")

            if request_id:
                gateway_payload = build_gateway_response(
                    request_id,
                    "success",
                    confirmation,
                    "Stock confirmado",
                )
                publish_event(ROUTING_KEY_GATEWAY_RESPONSE_SKILLS, gateway_payload)
                print(f"[inventario] published {ROUTING_KEY_GATEWAY_RESPONSE_SKILLS}: {gateway_payload}")
            return
        except ValueError as exc:
            confirmation = build_inventory_confirmation(order, False, str(exc))

    publish_event(ROUTING_KEY_INVENTORY_OUT_OF_STOCK, confirmation)
    print(f"[inventario] published {ROUTING_KEY_INVENTORY_OUT_OF_STOCK}: {confirmation}")

    if request_id:
        gateway_payload = build_gateway_response(
            request_id,
            "error",
            confirmation,
            str(exc),
        )
        publish_event(ROUTING_KEY_GATEWAY_RESPONSE_SKILLS, gateway_payload)
        print(f"[inventario] published {ROUTING_KEY_GATEWAY_RESPONSE_SKILLS}: {gateway_payload}")


def handle_skills_list(event: dict[str, Any]) -> None:
    request_id = event.get("request_id")
    skip = int(event.get("skip", 0))
    limit = int(event.get("limit", 100))

    print(f"[inventario] received {ROUTING_KEY_SKILLS_LIST}: {json.dumps(event, ensure_ascii=False)}")

    with SessionLocal() as db:
        skills = service.get_skills(db, skip=skip, limit=limit)
        skill_list = [serialize_skill(skill) for skill in skills]

    gateway_payload = {
        "request_id": request_id,
        "status": "success",
        "message": "Skills listadas",
        "result": skill_list,
        "skip": skip,
        "limit": limit,
        "count": len(skill_list),
    }
    publish_event(ROUTING_KEY_GATEWAY_RESPONSE_SKILLS_LIST, gateway_payload)
    print(f"[inventario] published {ROUTING_KEY_GATEWAY_RESPONSE_SKILLS_LIST}: {gateway_payload}")


def handle_event(message: dict[str, Any], routing_key: str) -> None:
    if routing_key == ROUTING_KEY_ORDER_CREATED:
        handle_order_created(message)
    elif routing_key == ROUTING_KEY_SKILLS_LIST:
        handle_skills_list(message)
    else:
        print(f"[inventario] no handler for routing key {routing_key}")


def run_inventory_service(mode: str = "run") -> None:
    if mode == "run":
        consume_forever(
            QUEUE_INVENTORY,
            [ROUTING_KEY_ORDER_CREATED, ROUTING_KEY_SKILLS_LIST],
            handle_event,
        )
        return

    processed = consume_once(QUEUE_INVENTORY, [ROUTING_KEY_ORDER_CREATED, ROUTING_KEY_SKILLS_LIST], handle_event)
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
