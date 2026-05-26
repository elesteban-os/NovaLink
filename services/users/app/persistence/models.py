"""SQLAlchemy ORM models for the users service.

Defines `User` and `UserSkill` models and their relationships.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """User ORM model representing application users."""

    __tablename__ = "users"

    # Identifier
    id = Column(Integer, primary_key=True, index=True)

    # User fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    skills = relationship(
        "UserSkill", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"


class UserSkill(Base):
    """UserSkill ORM model linking users to acquired skills and points."""

    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    skill_name = Column(String(255), nullable=False)
    points = Column(Integer, default=1, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="skills")

    def __repr__(self) -> str:
        return f"<UserSkill(user_id={self.user_id}, skill='{self.skill_name}', points={self.points})>"
