from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.logger import logger
from app.handlers import skills
from app.external.seed_skills import seed_skills


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja inicialización y cleanup de la aplicación.
    
    - Crea tablas en BD
    - Seed de datos
    - Cleanup al cerrar
    """
    logger.info(f"Iniciando {settings.API_TITLE}")
    
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas de BD creadas/verificadas")
    
    # Seed de datos
    try:
        seed_skills(reset=False)
        logger.info("Datos iniciales de skills sembrados")
    except Exception as e:
        logger.warning(f"No se pudieron seedear skills: {e}")
    
    yield
    
    logger.info("Cerrando aplicación")


# Crear aplicación
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(skills.router)

# Health check
@app.get("/health", tags=["health"])
def health_check():
    """Verificar estado de salud de la API."""
    return {
        "status": "ok",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION
    }

# Raíz
@app.get("/", tags=["info"])
def root():
    """Información de la API."""
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "docs": "/docs"
    }