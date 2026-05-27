"""Redis helper for the Skills microservice.

Provides a small API for idempotency and processing locks used by the
event consumer worker.
"""
from __future__ import annotations

import os
from typing import Any

try:
    import redis
except ImportError as exc:  # pragma: no cover - friendly runtime error
    raise SystemExit("Missing dependency: install redis with `pip install redis`." ) from exc


def get_redis_client() -> "redis.Redis":
    """Return a configured Redis client."""
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    try:
        return redis.Redis(host=host, port=port, decode_responses=True)
    except redis.ConnectionError as exc:  # pragma: no cover - runtime helper
        raise SystemExit("Could not connect to Redis. Start a Redis server or set REDIS_HOST/REDIS_PORT.") from exc


def _processing_key(service_name: str, event_id: str) -> str:
    return f"{service_name}:processing:{event_id}"


def _processed_key(service_name: str, event_id: str) -> str:
    return f"{service_name}:processed:{event_id}"


def is_order_processed(event_id: str, service_name: str = "skills") -> bool:
    client = get_redis_client()
    return client.exists(_processed_key(service_name, event_id)) == 1


def acquire_processing_lock(event_id: str, ttl: int = 30, service_name: str = "skills") -> bool:
    """Try to acquire a short processing lock for `event_id`.

    Returns True if the lock was acquired, False if another worker holds it.
    """
    client = get_redis_client()
    return client.set(_processing_key(service_name, event_id), "1", nx=True, ex=ttl) is True


def mark_order_processed(event_id: str, expire_seconds: int = 86400, service_name: str = "skills") -> None:
    client = get_redis_client()
    client.set(_processed_key(service_name, event_id), "1", ex=expire_seconds)
    # best-effort cleanup of processing lock
    client.delete(_processing_key(service_name, event_id))
