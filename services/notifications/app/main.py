from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .logger import logger
from .handlers.notifications import router as notifications_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Servicio de Notificaciones iniciado")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Servicio de Notificaciones detenido")


app = FastAPI(
    title="NovaLink - Servicio de Notificaciones",
    description="API REST para gestionar notificaciones de pedidos y asignación de habilidades",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notifications_router)
