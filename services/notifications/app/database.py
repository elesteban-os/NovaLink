"""PostgreSQL database connection and SQLAlchemy session utilities."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

# SQLAlchemy engine for notifications database
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
)

# Factory for SQLAlchemy database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy ORM models
Base = declarative_base()


def get_db():
    """Yield a database session instance and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
