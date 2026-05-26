"""CRUD operations for orders persistence.

Template for this service:
- Input: SQLAlchemy session, order payload, and authenticated `user_id`.
- Business logic: build and persist `Order` model.
- Output: persisted `Order` model instance.
"""

from sqlalchemy.orm import Session
from .models import Order
from .schemas import OrderCreate


def create_order(db: Session, user_id: int, order_data: OrderCreate) -> Order:
    """Persist a new order record and return the refreshed model."""

    db_order = Order(
        **order_data.model_dump(), user_id=user_id, issued_by="auth-service"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
