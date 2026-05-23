from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .logger import logger
from .handlers.orders import router as orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Servicio de Órdenes iniciado")
    yield
    logger.info("Servicio de Órdenes detenido")


# Crear la aplicación FastAPI
app = FastAPI(
    title="Servicio de Órdenes",
    description="Gestiona las órdenes de habilidades de los usuarios",
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

app.include_router(orders_router)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)
