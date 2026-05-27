"""Notification service example.

Template for this service:
- Message input: consume `usuario.actualizado` from the notifications queue.
- Business logic: build the final log in `log_confirmation`.
- Message output: no outgoing message; only write the confirmation log.

Run:
	python services/notifications/notifications.py run
	python services/notifications/notifications.py once
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
	QUEUE_NOTIFICATIONS,
	ROUTING_KEY_USER_UPDATED,
	consume_forever,
	consume_once,
)
from shared.redis_api import is_event_processed, mark_event_processed



def log_confirmation(user_update: dict[str, Any]) -> None:
	"""Print the final confirmation log for the user update event.

	This is the last step in the chain and it only writes a readable message to
	stdout so the flow can be verified easily.
	"""

	event_id = str(user_update.get("pedido_id", "unknown"))
	
	if is_event_processed(QUEUE_NOTIFICATIONS, event_id):
		print(f"[notificaciones] IGNORADO: El evento {event_id} ya fue procesado anteriormente.")
		return

	print(f"[notificaciones] received {ROUTING_KEY_USER_UPDATED}: {json.dumps(user_update, ensure_ascii=False)}")
	print(
		"[notificaciones] confirmation log: "
		f"pedido {user_update['pedido_id']} actualizado con {user_update['habilidad_asignada']}"
	)
	
	mark_event_processed(QUEUE_NOTIFICATIONS, event_id)


def run_notifications_service(mode: str = "run") -> None:
	"""Run the notifications service workflow."""

	if mode == "run":
		consume_forever(QUEUE_NOTIFICATIONS, ROUTING_KEY_USER_UPDATED, log_confirmation)
		return

	processed = consume_once(QUEUE_NOTIFICATIONS, ROUTING_KEY_USER_UPDATED, log_confirmation)
	if not processed:
		print(f"[notificaciones] no messages available in {QUEUE_NOTIFICATIONS}")


def build_parser() -> argparse.ArgumentParser:
	"""Build the command-line parser for the notifications service."""

	parser = argparse.ArgumentParser(description="NovaLink notification service example")
	parser.add_argument(
		"action",
		nargs="?",
		default="run",
		choices=["run", "once"],
		help="Run forever or process one message if available.",
	)
	return parser


def main() -> None:
	"""Run the notifications service in continuous or one-shot mode."""

	parser = build_parser()
	args = parser.parse_args()

	run_notifications_service(args.action)


if __name__ == "__main__":
	main()
