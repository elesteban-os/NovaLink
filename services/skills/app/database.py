"""Database engine, session factory and dependency provider for the skills service."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.config import settings
from app.logger import logger

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
)

# Sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM base
Base = declarative_base()


def get_db() -> Session:
    """
    Dependency to obtain a database session in endpoints.

    Usage in handlers:
        @app.get("/skills")
        def get_skills(db: Session = Depends(get_db)):
            return crud.get_skills(db)
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error en sesión BD: {e}")
        db.rollback()
        raise
    finally:
        db.close()
