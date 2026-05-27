from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class GatewayRequest(BaseModel):
    event_type: str
    payload: dict[str, Any] = Field(default_factory=dict)


class GatewayResult(BaseModel):
    request_id: str
    status: str
    payload: dict[str, Any] | None = None
    created_at: datetime
    completed_at: datetime | None = None
