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

app = FastAPI(
    title="Servicio de Órdenes",
    description="Gestiona las órdenes de habilidades de los usuarios",
    version="1.0.0",
    lifespan=lifespan
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

# ============================================================================
# GET /users/{user_id}/orders - Listar órdenes del usuario
# ============================================================================
@app.get(
    "/users/{user_id}/orders",
    response_model=OrderListResponse,
    summary="Listar órdenes del usuario",
    tags=["Órdenes"],
    responses={
        200: {"description": "Órdenes obtenidas exitosamente"},
        400: {"description": "ID de usuario inválido (debe ser > 0)"}
    }
)
def list_user_orders(
    user_id: int,
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(None, ge=1, description="Máximo de registros (None = todos)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las órdenes de un usuario específico, ordenadas por más recientes primero.
    
    - **user_id**: ID del usuario
    - **skip**: Número de registros a saltar (opcional, default=0)
    - **limit**: Número máximo de registros (opcional, default=None para todos)
    """
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="user_id debe ser mayor a 0")
    
    total = db.query(Order).filter(Order.user_id == user_id).count()
    query = db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).offset(skip)
    
    if limit is not None:
        query = query.limit(limit)
    
    orders = query.all()
    
    return {
        "total": total,
        "count": len(orders),
        "orders": orders
    }

# ============================================================================
# DELETE /orders/{order_id} - Eliminar orden
# ============================================================================
@app.delete(
    "/orders/{order_id}",
    status_code=204,
    summary="Eliminar orden",
    tags=["Órdenes"],
    responses={
        204: {"description": "Orden eliminada exitosamente"},
        404: {"description": "Orden no encontrada"}
    }
)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una orden específica por su ID.
    
    - **order_id**: ID de la orden a eliminar
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Orden {order_id} no encontrada")
    
    db.delete(order)
    db.commit()
    return None

# ============================================================================
# GET / - Health check
# ============================================================================
@app.get("/", tags=["Health"])
def health_check():
    """Verifica que el servicio esté activo."""
    return {"status": "healthy", "service": "orders"}
