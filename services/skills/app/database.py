from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.config import settings
from app.logger import logger

# Crear engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
)

# Sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para modelos ORM
Base = declarative_base()


def get_db() -> Session:
    """
    Dependencia para obtener sesión de BD en endpoints.
    
    Uso en handlers:
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
