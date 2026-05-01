from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query, Request, status
import jwt
import os
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Order
from schemas import OrderCreate, OrderResponse, OrderListResponse

# Create tables
Base.metadata.create_all(bind=engine)

SECRET_KEY = os.getenv("JWT_SECRET", "SUPER_SECRET_KEY")
ALGORITHM = "HS256"

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

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
    request: Request,
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva orden vinculada a un usuario basado en el token.
    
    - **skill_name**: Nombre de la habilidad (no puede estar solo de espacios)
    - **quantity**: Cantidad solicitada (debe ser > 0)
    """
    user_id = verify_token(request)
    db_order = Order(**order.model_dump(), user_id=user_id, issued_by="auth-service")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
