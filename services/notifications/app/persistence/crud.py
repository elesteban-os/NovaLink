"""Database CRUD operations for notifications."""

from sqlalchemy.orm import Session
from .models import Notification
from .schemas import NotificationCreate


def create_notification(db: Session, notification_data: NotificationCreate) -> Notification:
    """Persist a notification record and refresh it with generated fields."""
    db_notification = Notification(
        user_id=notification_data.user_id,
        order_id=notification_data.order_id,
        title=notification_data.title,
        description=notification_data.description,
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
