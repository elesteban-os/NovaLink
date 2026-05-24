"""Database CRUD operations for the Auth service."""

from sqlalchemy.orm import Session

from app.persistence.models import User
from app.logger import logger


def get_user_by_email(db: Session, email: str) -> User | None:
    """Return a user record that matches the given email address."""
    user = db.query(User).filter(User.email == email).first()
    if user:
        logger.info(f"User found by email: {email}")
    else:
        logger.info(f"User not found by email: {email}")
    return user
