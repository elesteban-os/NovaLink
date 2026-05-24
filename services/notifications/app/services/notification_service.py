"""Notification business logic service."""

from sqlalchemy.orm import Session

from ..persistence.crud import create_notification as create_notification_db
from ..email_service import send_email
from ..logger import logger
from ..persistence.schemas import NotificationCreate


def create_notification(db: Session, notification_data: NotificationCreate):
    """Create a notification in the database and send a simulated email."""
    db_notification = create_notification_db(db, notification_data)
    logger.info(
        "Notificacion creada: id=%s user_id=%s order_id=%s title=%s",
        db_notification.id,
        db_notification.user_id,
        db_notification.order_id,
        db_notification.title,
    )
    send_email(db_notification)
    return db_notification
