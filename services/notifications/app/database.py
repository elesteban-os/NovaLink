"""
Configuración de la conexión a PostgreSQL y sesiones de SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

# Motor de SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
)

# Factory para crear sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """Generador de dependencia para obtener la sesión de la base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
