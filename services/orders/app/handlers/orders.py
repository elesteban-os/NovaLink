"""HTTP handlers for the orders service.

Template for this service:
- Endpoint input: POST `/orders` with `OrderCreate`.
- Business logic: verify token and create order using `create_order_service`.
- Endpoint output: return persisted `OrderResponse`.

"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..core.security import verify_token
from ..database import get_db
from ..persistence.schemas import OrderCreate, OrderResponse
from ..services.order_service import create_order as create_order_service

router = APIRouter(tags=["orders"])


@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201,
    summary="Crear nueva orden",
    responses={
        201: {"description": "Orden creada exitosamente"},
        422: {
            "description": "Validación fallida: user_id > 0, quantity > 0, skill_name 1-255 chars"
        },
    },
)
def create_order(
    request: Request,
    order: OrderCreate,
    db: Session = Depends(get_db),
):
    """Validate auth token, create the order, and return saved order data."""

    user_id = verify_token(request)
    return create_order_service(db, user_id, order)
