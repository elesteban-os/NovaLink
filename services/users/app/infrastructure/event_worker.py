"""Event consumer worker for the Users microservice."""

from __future__ import annotations

import argparse
import json
from typing import Any

from app.database import SessionLocal
from app.persistence.schemas import UserCreate, UserSkillCreate
from app.infrastructure.rabbitmq import (
    QUEUE_USERS,
    ROUTING_KEY_INVENTORY_CONFIRMED,
    ROUTING_KEY_USER_CREATE,
    ROUTING_KEY_USER_SKILLS_LIST,
    ROUTING_KEY_USERS_LIST,
    ROUTING_KEY_USER_UPDATED,
    ROUTING_KEY_GATEWAY_RESPONSE_USERS,
    ROUTING_KEY_GATEWAY_RESPONSE_USERS_LIST,
    ROUTING_KEY_GATEWAY_RESPONSE_USERS_SKILLS,
    consume_forever,
    consume_once,
    publish_event,
)
from app.services.user_service import user_service


def build_user_updated_event(inventory_event: dict[str, Any], assigned: bool, reason: str | None = None) -> dict[str, Any]:
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


def serialize_user(user: Any) -> dict[str, Any]:
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }


def serialize_user_skill(skill: Any) -> dict[str, Any]:
    return {
        "id": skill.id,
        "user_id": skill.user_id,
        "skill_name": skill.skill_name,
        "points": skill.points,
        "created_at": skill.created_at,
        "updated_at": skill.updated_at,
    }


def build_gateway_response(request_id: str | None, status: str, payload: dict[str, Any], message: str) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "status": status,
        "message": message,
        "result": payload,
    }


def handle_inventory_confirmed(inventory_event: dict[str, Any]) -> None:
    print(
        f"[usuarios] received {ROUTING_KEY_INVENTORY_CONFIRMED}: "
        f"{json.dumps(inventory_event, ensure_ascii=False)}"
    )

    request_id = inventory_event.get("request_id")
    assigned = False
    reason: str | None = None
    if inventory_event.get("stock_validado"):
        with SessionLocal() as db:
            try:
                skill_data = UserSkillCreate(skill_name=inventory_event["skill_name"], points=1)
                user_service.add_user_skill(db, inventory_event["user_id"], skill_data)
                assigned = True
            except ValueError as exc:
                reason = str(exc)
    else:
        reason = inventory_event.get("motivo") or "Stock insuficiente o skill no disponible"

    user_update = build_user_updated_event(inventory_event, assigned, reason)
    publish_event(ROUTING_KEY_USER_UPDATED, user_update)
    print(f"[usuarios] published {ROUTING_KEY_USER_UPDATED}: {user_update}")

    if request_id:
        gateway_payload = build_gateway_response(
            request_id,
            "success" if assigned else "error",
            user_update,
            "Usuario actualizado" if assigned else "Actualización de usuario pendiente",
        )
        publish_event(ROUTING_KEY_GATEWAY_RESPONSE_USERS, gateway_payload)
        print(f"[usuarios] published {ROUTING_KEY_GATEWAY_RESPONSE_USERS}: {gateway_payload}")


def handle_user_create(event: dict[str, Any]) -> None:
    request_id = event.get("request_id")
    user_payload = {k: v for k, v in event.items() if k != "request_id"}

    print(f"[usuarios] received {ROUTING_KEY_USER_CREATE}: {json.dumps(event, ensure_ascii=False)}")

    with SessionLocal() as db:
        try:
            user = user_service.create_user(db, UserCreate(**user_payload))
            result = serialize_user(user)
            status = "success"
            message = "Usuario creado"
        except ValueError as exc:
            result = {"error": str(exc)}
            status = "error"
            message = str(exc)

    if request_id:
        gateway_payload = build_gateway_response(request_id, status, result, message)
        publish_event(ROUTING_KEY_GATEWAY_RESPONSE_USERS, gateway_payload)
        print(f"[usuarios] published {ROUTING_KEY_GATEWAY_RESPONSE_USERS}: {gateway_payload}")


def handle_users_list(event: dict[str, Any]) -> None:
    request_id = event.get("request_id")
    skip = int(event.get("skip", 0))
    limit = int(event.get("limit", 100))

    print(f"[usuarios] received {ROUTING_KEY_USERS_LIST}: {json.dumps(event, ensure_ascii=False)}")

    with SessionLocal() as db:
        users = user_service.get_users(db, skip=skip, limit=limit)
        result = [serialize_user(user) for user in users]

    gateway_payload = {
        "request_id": request_id,
        "status": "success",
        "message": "Usuarios listados",
        "result": result,
        "skip": skip,
        "limit": limit,
        "count": len(result),
    }
    publish_event(ROUTING_KEY_GATEWAY_RESPONSE_USERS_LIST, gateway_payload)
    print(f"[usuarios] published {ROUTING_KEY_GATEWAY_RESPONSE_USERS_LIST}: {gateway_payload}")


def handle_user_skills_list(event: dict[str, Any]) -> None:
    request_id = event.get("request_id")
    user_id = int(event.get("user_id", 0))

    print(f"[usuarios] received {ROUTING_KEY_USER_SKILLS_LIST}: {json.dumps(event, ensure_ascii=False)}")

    with SessionLocal() as db:
        try:
            skills = user_service.get_user_skills(db, user_id)
            result = [serialize_user_skill(skill) for skill in skills]
            status = "success"
            message = "Habilidades listadas"
        except ValueError as exc:
            result = {"error": str(exc)}
            status = "error"
            message = str(exc)

    gateway_payload = build_gateway_response(request_id, status, result, message)
    publish_event(ROUTING_KEY_GATEWAY_RESPONSE_USERS_SKILLS, gateway_payload)
    print(f"[usuarios] published {ROUTING_KEY_GATEWAY_RESPONSE_USERS_SKILLS}: {gateway_payload}")


def handle_event(message: dict[str, Any], routing_key: str) -> None:
    if routing_key == ROUTING_KEY_INVENTORY_CONFIRMED:
        handle_inventory_confirmed(message)
    elif routing_key == ROUTING_KEY_USER_CREATE:
        handle_user_create(message)
    elif routing_key == ROUTING_KEY_USERS_LIST:
        handle_users_list(message)
    elif routing_key == ROUTING_KEY_USER_SKILLS_LIST:
        handle_user_skills_list(message)
    else:
        print(f"[usuarios] no handler for routing key {routing_key}")


def run_users_service(mode: str = "run") -> None:
    if mode == "run":
        consume_forever(
            QUEUE_USERS,
            [
                ROUTING_KEY_INVENTORY_CONFIRMED,
                ROUTING_KEY_USER_CREATE,
                ROUTING_KEY_USERS_LIST,
                ROUTING_KEY_USER_SKILLS_LIST,
            ],
            handle_event,
        )
        return

    processed = consume_once(
        QUEUE_USERS,
        [
            ROUTING_KEY_INVENTORY_CONFIRMED,
            ROUTING_KEY_USER_CREATE,
            ROUTING_KEY_USERS_LIST,
            ROUTING_KEY_USER_SKILLS_LIST,
        ],
        handle_event,
    )
    if not processed:
        print(f"[usuarios] no messages disponible en {QUEUE_USERS}")


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
