from __future__ import annotations

import os
from datetime import datetime, timedelta
from threading import Lock
from typing import Any

DEFAULT_TTL_SECONDS = 300


def _current_time() -> datetime:
    return datetime.utcnow()


class ResponseStore:
    def __init__(self) -> None:
        self.ttl = int(os.getenv("GATEWAY_RESULT_TTL_SECONDS", DEFAULT_TTL_SECONDS))
        self._lock = Lock()
        self._records: dict[str, dict[str, Any]] = {}

    def create_request(self, request_id: str) -> None:
        with self._lock:
            self._records[request_id] = {
                "request_id": request_id,
                "status": "pending",
                "payload": None,
                "created_at": _current_time(),
                "completed_at": None,
            }

    def set_result(self, request_id: str, payload: dict[str, Any]) -> None:
        with self._lock:
            record = self._records.get(request_id)
            if record is None:
                record = {
                    "request_id": request_id,
                    "status": "pending",
                    "payload": None,
                    "created_at": _current_time(),
                    "completed_at": None,
                }
            record.update(
                {
                    "status": "done",
                    "payload": payload,
                    "completed_at": _current_time(),
                }
            )
            self._records[request_id] = record

    def get_result(self, request_id: str) -> dict[str, Any] | None:
        self._cleanup_expired()
        with self._lock:
            record = self._records.get(request_id)
            return dict(record) if record is not None else None

    def _cleanup_expired(self) -> None:
        threshold = _current_time() - timedelta(seconds=self.ttl)
        with self._lock:
            expired_keys = [key for key, record in self._records.items() if record["created_at"] < threshold]
            for key in expired_keys:
                del self._records[key]


response_store = ResponseStore()
