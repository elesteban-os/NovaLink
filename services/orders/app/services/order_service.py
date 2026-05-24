"""Order business logic for the orders service.

Template for this service:
- Input: DB session, authenticated `user_id`, and `OrderCreate`.
- Business logic: persist order using `create_order_db` and log creation.
- Output: returned `Order` ORM object.
"""

from sqlalchemy.orm import Session

from ..persistence.crud import create_order as create_order_db
from ..logger import logger
from ..persistence.schemas import OrderCreate


def create_order(db: Session, user_id: int, order_data: OrderCreate):
    """Create a new order and persist it in the database."""
    db_order = create_order_db(db, user_id, order_data)
    logger.info(
        "Orden creada: id=%s user_id=%s skill_name=%s quantity=%s",
        db_order.id,
        db_order.user_id,
        db_order.skill_name,
        db_order.quantity,
    )
    return db_order
