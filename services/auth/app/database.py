import time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.config import settings
from app.logger import logger

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def wait_for_db(max_retries: int = 10, delay_seconds: float = 1.0) -> None:
    """Esperar a que la base de datos PostgreSQL esté disponible."""
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as connection:
                logger.info("Database connection established")
                return
        except OperationalError as exc:
            logger.warning(
                f"Database unavailable (attempt {attempt}/{max_retries}): {exc}"
            )
            if attempt == max_retries:
                logger.error("Database connection failed after retries")
                raise
            time.sleep(delay_seconds)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    except Exception as exc:
        logger.error(f"Database session error: {exc}")
        raise
    finally:
        db.close()
