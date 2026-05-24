"""Skills service FastAPI application.

Template for this service:
- Endpoint input: CRUD operations under `/skills`.
- Business logic: process skill commands in `SkillService`.
- Endpoint output: return `SkillResponse` models or health info.
"""

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
    Handle application startup and shutdown.
    
    - Create database tables
    - Seed initial data
    - Cleanup on shutdown
    """
    logger.info(f"Starting {settings.API_TITLE}")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    
    # Seed initial data
    try:
        seed_skills(reset=False)
        logger.info("Datos iniciales de skills sembrados")
    except Exception as e:
        logger.warning(f"Could not seed skills: {e}")
    
    yield
    
    logger.info("Shutting down application")


# Create application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(skills.router)

# Health check
@app.get("/health", tags=["health"])
def health_check():
    """Check API health status."""
    return {
        "status": "ok",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION
    }

# Root
@app.get("/", tags=["info"])
def root():
    """API information."""
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "docs": "/docs"
    }