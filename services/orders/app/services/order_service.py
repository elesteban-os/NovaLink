from sqlalchemy.orm import Session

from ..persistence.crud import create_order as create_order_db
from ..logger import logger
from ..persistence.schemas import OrderCreate
from app.rabbitmq import publish_event, ROUTING_KEY_ORDER_CREATED


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

    publish_event(
        ROUTING_KEY_ORDER_CREATED,
        {
            "pedido_id": db_order.id,
            "user_id": db_order.user_id,
            "skill_name": db_order.skill_name,
            "quantity": db_order.quantity,
            "issued_by": db_order.issued_by,
        },
    )
    logger.info("Published pedido.creado event for order id=%s", db_order.id)
    return db_order
