"""Users service FastAPI application.

Template for this service:
- Endpoint input: CRUD under `/users` and skill management under `/users/{id}/skills`.
- Business logic: handled in `UserService` in `services/user_service.py`.
- Endpoint output: return `UserResponse` and `UserSkillResponse` models.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.external.seed_users import seed_users
from app.handlers.users import router as users_router
from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Users Microservice")
    Base.metadata.create_all(bind=engine)
    seed_users()
    yield
    logger.info("Shutting down Users Microservice")


app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
    }


@app.get("/")
def root():
    return {
        "message": "Users Microservice is running",
        "api_version": settings.API_VERSION,
    }
