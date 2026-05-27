"""Event consumer worker for the Orders microservice."""

from __future__ import annotations

import argparse
import json
from typing import Any

from app.infrastructure.rabbitmq import (
    QUEUE_INVENTORY_OUT_OF_STOCK,
    ROUTING_KEY_INVENTORY_OUT_OF_STOCK,
    consume_forever,
    consume_once,
)
from app.infrastructure.redis import (
    acquire_processing_lock,
    is_event_processed,
    mark_event_processed,
)


def handle_inventory_out_of_stock(event: dict[str, Any]) -> None:
    print(
        f"[orders] received {ROUTING_KEY_INVENTORY_OUT_OF_STOCK}: "
        f"{json.dumps(event, ensure_ascii=False)}"
    )
    print(
        "[orders] inventory denied the order due to out-of-stock or insufficient stock. "
        "Consider adding order state handling in the database if you want to track failures."
    )

    event_id = event.get("pedido_id")
    if not event_id:
        print("[orders] missing pedido_id in message, skipping idempotency checks")
        return

    if is_event_processed(event_id):
        print(f"[orders] already processed {event_id}, skipping")
        return

    if not acquire_processing_lock(event_id, ttl=30):
        print(f"[orders] another worker is processing {event_id}, skipping")
        return

    # At this point we can perform order failure handling (e.g., update DB).
    # The current worker only logs; mark the event as processed to avoid duplicates.
    mark_event_processed(event_id)


def run_orders_service(mode: str = "run") -> None:
    if mode == "run":
        consume_forever(
            QUEUE_INVENTORY_OUT_OF_STOCK,
            ROUTING_KEY_INVENTORY_OUT_OF_STOCK,
            handle_inventory_out_of_stock,
        )
        return

    processed = consume_once(
        QUEUE_INVENTORY_OUT_OF_STOCK,
        ROUTING_KEY_INVENTORY_OUT_OF_STOCK,
        handle_inventory_out_of_stock,
    )
    if not processed:
        print(f"[orders] no messages available in {QUEUE_INVENTORY_OUT_OF_STOCK}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NovaLink orders event worker")
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
    run_orders_service(args.action)


if __name__ == "__main__":
    main()
