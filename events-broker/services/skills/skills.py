"""Inventory service example.

Template for this service:
- Message input: consume `pedido.creado` from the inventory queue.
- Business logic: validate the order in `validate_stock`.
- Message output: publish `inventario.confirmado` in `handle_order_created`.

This file is named skills.py because that is the file provided in the folder.
Its role in the flow is the inventory step.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent.parent
if str(ROOT_DIR) not in sys.path:
	sys.path.insert(0, str(ROOT_DIR))

from shared.rabbitmq_api import (
	QUEUE_INVENTORY,
	ROUTING_KEY_INVENTORY_CONFIRMED,
	ROUTING_KEY_ORDER_CREATED,
	consume_forever,
	consume_once,
	publish_event,
)
from shared.redis_api import is_event_processed, mark_event_processed



def validate_stock(order: dict[str, Any]) -> dict[str, Any]:
	"""Build the inventory confirmation payload from the received order.

	The example does not perform real stock lookup; it simply marks the order as
	validated and keeps the essential fields for the next service.
	"""

	return {
		"pedido_id": order["pedido_id"],
		"cliente": order["cliente"],
		"producto": order["producto"],
		"cantidad": order["cantidad"],
		"stock_validado": True,
		"inventario_estado": "confirmado",
	}


def handle_order_created(order: dict[str, Any]) -> None:
	"""Handle `pedido.creado`, log it, and publish `inventario.confirmado`."""
	
	# Usamos el pedido_id como identificador de idempotencia
	event_id = str(order.get("pedido_id", "unknown"))
	
	if is_event_processed(QUEUE_INVENTORY, event_id):
		print(f"[inventario] IGNORADO: El evento {event_id} ya fue procesado anteriormente.")
		return

	print(f"[inventario] received {ROUTING_KEY_ORDER_CREATED}: {json.dumps(order, ensure_ascii=False)}")
	confirmation = validate_stock(order)
	publish_event(ROUTING_KEY_INVENTORY_CONFIRMED, confirmation)
	
	# Registramos el evento en caché para evitar procesarlo de nuevo en el futuro
	mark_event_processed(QUEUE_INVENTORY, event_id)
	print(f"[inventario] published {ROUTING_KEY_INVENTORY_CONFIRMED}: {confirmation}")


def run_inventory_service(mode: str = "run") -> None:
	"""Run the inventory service in continuous or one-shot mode."""

	if mode == "run":
		consume_forever(QUEUE_INVENTORY, ROUTING_KEY_ORDER_CREATED, handle_order_created)
		return

	processed = consume_once(QUEUE_INVENTORY, ROUTING_KEY_ORDER_CREATED, handle_order_created)
	if not processed:
		print(f"[inventario] no messages available in {QUEUE_INVENTORY}")


def build_parser() -> argparse.ArgumentParser:
	"""Build the command-line parser for the inventory step."""

	parser = argparse.ArgumentParser(description="NovaLink inventory service example")
	parser.add_argument(
		"action",
		nargs="?",
		default="run",
		choices=["run", "once"],
		help="Run forever or process one message if available.",
	)
	return parser


def main() -> None:
	"""Run the inventory service in continuous or one-shot mode."""

	parser = build_parser()
	args = parser.parse_args()

	run_inventory_service(args.action)


if __name__ == "__main__":
	main()
