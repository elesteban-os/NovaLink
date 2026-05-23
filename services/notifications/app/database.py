"""
Configuración de la conexión a PostgreSQL y sesiones de SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Construcción de la URL de conexión a PostgreSQL
DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

# Motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv('DB_ECHO', 'false').lower() == 'true'
)

# Factory para crear sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Generador de dependencia para obtener la sesión de la base de datos.
    Se utiliza en los endpoints de FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
