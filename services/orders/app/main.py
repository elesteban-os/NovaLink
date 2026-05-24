"""Order service FastAPI application.

Template for this service:
- Endpoint input: POST `/orders` with `OrderCreate`.
- Business logic: create order in `create_order` service.
- Endpoint output: return `OrderResponse`.

"""

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


# Create FastAPI application
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

# Create database tables
Base.metadata.create_all(bind=engine)
