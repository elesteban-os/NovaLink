from sqlalchemy.orm import Session
from .models import Order
from .schemas import OrderCreate


def create_order(db: Session, user_id: int, order_data: OrderCreate) -> Order:
    db_order = Order(**order_data.model_dump(), user_id=user_id, issued_by="auth-service")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
