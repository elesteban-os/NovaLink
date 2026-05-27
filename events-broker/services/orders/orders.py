"""Order service example.

Template for this service:
- Message input: none. This is the initial producer.
- Business logic: build the order payload in `build_sample_order`.
- Message output: publish `pedido.creado` in `publish_sample_order`.

Run:
	python services/orders/orders.py publish
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.rabbitmq_api import ROUTING_KEY_ORDER_CREATED, publish_event
from shared.redis_api import is_event_processed, mark_event_processed


def build_sample_order() -> dict[str, Any]:
    """Create the hardcoded order payload used to start the example flow.

    This is the only data the orders service produces in this example.
    """

    return {
        "pedido_id": 1001,
        "cliente": "cliente_demo",
        "producto": "teclado",
        "cantidad": 2,
        "total": 49.99,
        "estado": "creado",
    }


def publish_sample_order() -> None:
    """Publish the hardcoded order to the `pedido.creado` event."""

	payload = build_sample_order()
	
	# Usamos un identificador único para el intento de pedido
	idempotency_key = f"{payload['cliente']}_{payload['pedido_id']}"
	
	if is_event_processed("orders_publisher", idempotency_key):
		print(f"[orders] COMPRA IGNORADA: La transacción para el pedido {payload['pedido_id']} ya fue enviada anteriormente para evitar cobros dobles.")
		return

	publish_event(ROUTING_KEY_ORDER_CREATED, payload)
	
	# Registrar el pedido como creado y enviado
	mark_event_processed("orders_publisher", idempotency_key)
	print(f"[orders] published {ROUTING_KEY_ORDER_CREATED}: {payload}")


def run_orders_service() -> None:
    """Run the orders service workflow."""

    publish_sample_order()


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for the orders service."""

    parser = argparse.ArgumentParser(description="NovaLink order service example")
    parser.add_argument(
        "action",
        nargs="?",
        default="publish",
        choices=["publish"],
        help="Action to run. The order service only publishes the initial event.",
    )
    return parser


def main() -> None:
    """Run the orders service entrypoint."""

    parser = build_parser()
    args = parser.parse_args()

    if args.action == "publish":
        run_orders_service()


if __name__ == "__main__":
    main()
