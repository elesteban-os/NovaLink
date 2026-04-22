from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Order
from schemas import OrderCreate, OrderResponse, OrderListResponse

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[INICIO]")
    yield
    print("[FIN]")

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Servicio de Órdenes",
    description="Gestiona las órdenes de habilidades de los usuarios",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# POST /orders - Crear nueva orden
# ============================================================================
@app.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201,
    summary="Crear nueva orden",
    tags=["Órdenes"],
    responses={
        201: {"description": "Orden creada exitosamente"},
        422: {"description": "Validación fallida: user_id > 0, quantity > 0, skill_name 1-255 chars"}
    }
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva orden vinculada a un usuario.
    
    - **user_id**: ID del usuario (debe ser > 0)
    - **skill_name**: Nombre de la habilidad (no puede estar solo de espacios)
    - **quantity**: Cantidad solicitada (debe ser > 0)
    """
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
