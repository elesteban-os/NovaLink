from threading import Thread

from app.infrastructure.rabbitmq import (
    QUEUE_GATEWAY_RESPONSES,
    ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS,
    ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS_LIST,
    ROUTING_KEY_GATEWAY_RESPONSE_SKILLS,
    ROUTING_KEY_GATEWAY_RESPONSE_SKILLS_LIST,
    ROUTING_KEY_GATEWAY_RESPONSE_USERS,
    ROUTING_KEY_GATEWAY_RESPONSE_USERS_LIST,
    ROUTING_KEY_GATEWAY_RESPONSE_USERS_SKILLS,
    consume_forever,
)
from app.infrastructure.storage import response_store


def handle_gateway_response(message: dict[str, object], routing_key: str) -> None:
    request_id = message.get("request_id")
    if not request_id:
        print("[gateway] received response without request_id, ignoring")
        return

    response_store.set_result(request_id, dict(message))
    print(f"[gateway] stored response for request_id={request_id} via {routing_key}")


def start_gateway_response_consumer() -> None:
    routing_keys = [
        ROUTING_KEY_GATEWAY_RESPONSE_SKILLS,
        ROUTING_KEY_GATEWAY_RESPONSE_SKILLS_LIST,
        ROUTING_KEY_GATEWAY_RESPONSE_USERS,
        ROUTING_KEY_GATEWAY_RESPONSE_USERS_LIST,
        ROUTING_KEY_GATEWAY_RESPONSE_USERS_SKILLS,
        ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS,
        ROUTING_KEY_GATEWAY_RESPONSE_NOTIFICATIONS_LIST,
    ]

    consumer_thread = Thread(
        target=consume_forever,
        args=(QUEUE_GATEWAY_RESPONSES, routing_keys, handle_gateway_response),
        daemon=True,
    )
    consumer_thread.start()
