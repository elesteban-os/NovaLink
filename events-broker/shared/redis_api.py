"""Shared Redis API for managing state and idempotency.

This module provides an easy way for services to interact with a shared
Redis cluster to prevent processing duplicate messages (idempotency).
"""

from __future__ import annotations

import os

try:
	import redis
except ImportError as exc:
	raise SystemExit("Missing dependency: install redis with `pip install redis`.") from exc

def get_redis_client() -> redis.Redis:
	"""Return a configured Redis client."""
	host = os.getenv("REDIS_HOST", "localhost")
	port = int(os.getenv("REDIS_PORT", "6379"))
	
	try:
		# decode_responses=True ensures strings instead of bytes are returned
		return redis.Redis(host=host, port=port, decode_responses=True)
	except redis.ConnectionError as exc:
		raise SystemExit(
			"Could not connect to Redis. Start the broker first with:\n"
			"  docker compose -f events-broker/docker-compose.yml up -d"
		) from exc

def is_event_processed(service_name: str, event_id: str) -> bool:
	"""Check if an event was already processed by this service."""
	client = get_redis_client()
	key = f"processed:{service_name}:{event_id}"
	return client.exists(key) > 0

def mark_event_processed(service_name: str, event_id: str, expire_seconds: int = 86400) -> None:
	"""Mark an event as processed with an expiration time (default 24h)."""
	client = get_redis_client()
	key = f"processed:{service_name}:{event_id}"
	client.set(key, "1", ex=expire_seconds)
