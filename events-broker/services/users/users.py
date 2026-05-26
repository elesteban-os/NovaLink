"""User service example.

Template for this service:
- Message input: consume `inventario.confirmado` from the users queue.
- Business logic: assign the skill in `assign_skill`.
- Message output: publish `usuario.actualizado` in `handle_inventory_confirmed`.

Run:
	python services/users/users.py run
	python services/users/users.py once
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
	QUEUE_USERS,
	ROUTING_KEY_INVENTORY_CONFIRMED,
	ROUTING_KEY_USER_UPDATED,
	consume_forever,
	consume_once,
	publish_event,
)
from shared.redis_api import is_event_processed, mark_event_processed



def assign_skill(inventory_confirmation: dict[str, Any]) -> dict[str, Any]:
	"""Create the user update payload that follows the inventory confirmation.

	In this example the service just assigns a fixed skill and forwards the
	important values to the next event.
	"""

	return {
		"pedido_id": inventory_confirmation["pedido_id"],
		"cliente": inventory_confirmation["cliente"],
		"habilidad_asignada": "habilidad_demo",
		"usuario_estado": "actualizado",
		"inventario_confirmado": inventory_confirmation["stock_validado"],
	}


def handle_inventory_confirmed(inventory_confirmation: dict[str, Any]) -> None:
	"""Handle `inventario.confirmado` and publish `usuario.actualizado`."""

	event_id = str(inventory_confirmation.get("pedido_id", "unknown"))
	
	if is_event_processed(QUEUE_USERS, event_id):
		print(f"[usuarios] IGNORADO: El evento {event_id} ya fue procesado anteriormente.")
		return

	print(
		f"[usuarios] received {ROUTING_KEY_INVENTORY_CONFIRMED}: "
		f"{json.dumps(inventory_confirmation, ensure_ascii=False)}"
	)
	user_update = assign_skill(inventory_confirmation)
	publish_event(ROUTING_KEY_USER_UPDATED, user_update)
	
	mark_event_processed(QUEUE_USERS, event_id)
	print(f"[usuarios] published {ROUTING_KEY_USER_UPDATED}: {user_update}")


def run_users_service(mode: str = "run") -> None:
	"""Run the users service workflow."""

	if mode == "run":
		consume_forever(QUEUE_USERS, ROUTING_KEY_INVENTORY_CONFIRMED, handle_inventory_confirmed)
		return

	processed = consume_once(QUEUE_USERS, ROUTING_KEY_INVENTORY_CONFIRMED, handle_inventory_confirmed)
	if not processed:
		print(f"[usuarios] no messages available in {QUEUE_USERS}")


def build_parser() -> argparse.ArgumentParser:
	"""Build the command-line parser for the users service."""

	parser = argparse.ArgumentParser(description="NovaLink user service example")
	parser.add_argument(
		"action",
		nargs="?",
		default="run",
		choices=["run", "once"],
		help="Run forever or process one message if available.",
	)
	return parser


def main() -> None:
	"""Run the users service in continuous or one-shot mode."""

	parser = build_parser()
	args = parser.parse_args()

	run_users_service(args.action)


if __name__ == "__main__":
	main()
