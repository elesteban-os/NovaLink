from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.infrastructure.rabbitmq import publish_event
from app.infrastructure.storage import response_store
from app.models import GatewayRequest, GatewayResult

router = APIRouter(prefix="/api/gateway", tags=["gateway"])


@router.post("/request", status_code=202)
def create_request(request: GatewayRequest) -> dict[str, str]:
    request_id = str(uuid4())
    payload = request.payload.copy()
    payload["request_id"] = request_id

    publish_event(request.event_type, payload)
    response_store.create_request(request_id)

    return {"request_id": request_id, "status": "pending"}


@router.get("/result/{request_id}", response_model=GatewayResult)
def get_result(request_id: str) -> GatewayResult:
    result = response_store.get_result(request_id)
    if result is None:
        raise HTTPException(status_code=404, detail="request_id not found or expired")

    return GatewayResult(**result)
