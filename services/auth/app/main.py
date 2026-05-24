from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine, wait_for_db
from app.handlers.auth import router as auth_router
from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Auth Microservice")
    wait_for_db()
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down Auth Microservice")


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

app.include_router(auth_router)


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
        "message": "Auth Microservice is running",
        "api_version": settings.API_VERSION,
    }
