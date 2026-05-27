"""Database CRUD operations for notifications."""

from typing import List

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


def get_notifications(db: Session, user_id: int | None = None) -> List[Notification]:
    """Return stored notifications, optionally filtered by user."""
    query = db.query(Notification)
    if user_id is not None:
        query = query.filter(Notification.user_id == user_id)
    return query.order_by(Notification.created_at.desc()).all()
