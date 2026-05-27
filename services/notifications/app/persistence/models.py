"""SQLAlchemy models for notifications storage."""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base


class Notification(Base):
    """Database model representing a user notification."""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    order_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        """Return a compact string representation of the notification."""
        return f"<Notification(id={self.id}, user_id={self.user_id}, order_id={self.order_id})>"
