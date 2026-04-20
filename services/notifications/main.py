"""
Microservicio de Notificaciones - FastAPI
Endpoints REST para crear, listar y eliminar notificaciones.
Integración con simulación de envío de email.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import Base, engine, get_db
from models import Notification
from schemas import NotificationCreate, NotificationResponse, NotificationListResponse
from email_service import send_email
from contextlib import asynccontextmanager

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)


# Evento de startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicacion.
    Se ejecuta al inicio y al cierre.
    """
    print("[INICIO] Servicio de Notificaciones iniciado")
    yield
    print("[FIN] Servicio de Notificaciones detenido")


# Crear la aplicación FastAPI
app = FastAPI(
    title="NovaLink - Servicio de Notificaciones",
    description="API REST para gestionar notificaciones de pedidos y asignación de habilidades",
    version="1.0.0",
    lifespan=lifespan
)


# ==================== ENDPOINTS ====================

@app.post(
    "/notifications",
    response_model=NotificationResponse,
    status_code=201,
    summary="Crear nueva notificación",
    tags=["Notificaciones"],
    responses={
        201: {"description": "Notificación creada exitosamente"},
        422: {"description": "Validación fallida: user_id > 0, order_id > 0, title 1-255 caracteres, description no vacía"}
    }
)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva notificación y simula envío de email.
    
    Validaciones: user_id y order_id > 0, title 1-255 chars, description >= 1 char.
    """
    
    # Crear nueva notificación
    db_notification = Notification(
        user_id=notification.user_id,
        order_id=notification.order_id,
        title=notification.title,
        description=notification.description
    )
    
    # Guardar en la base de datos
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    
    # Simular envio de notificacion por email
    # En produccion, esto integraria con un servicio de email real
    send_email(db_notification)
    
    return db_notification


@app.get(
    "/users/{user_id}/notifications",
    response_model=NotificationListResponse,
    summary="Obtener notificaciones de un usuario",
    tags=["Notificaciones"],
    responses={
        200: {"description": "Notificaciones del usuario obtenidas exitosamente"},
        400: {"description": "El ID del usuario debe ser positivo (user_id > 0)"},
        422: {"description": "Parámetros de query inválidos: skip >= 0, limit >= 1"}
    }
)
def get_user_notifications(
    user_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(None, ge=1, description="Número máximo de registros (None = todos)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene las notificaciones de un usuario.
    
    Por defecto devuelve todas las notificaciones ordenadas por más recientes primero.
    Opcionalmente, soporta paginación mediante skip y limit.
    """
    
    # Validar que user_id sea positivo
    if user_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="El ID del usuario debe ser positivo"
        )
    
    # Obtener total de notificaciones del usuario
    total = db.query(Notification).filter(
        Notification.user_id == user_id
    ).count()
    
    # Obtener notificaciones del usuario
    query = db.query(Notification).filter(
        Notification.user_id == user_id
    ).order_by(desc(Notification.created_at)).offset(skip)
    
    # Aplicar limit solo si se proporciona
    if limit is not None:
        query = query.limit(limit)
    
    notifications = query.all()
    
    return {
        "total": total,
        "count": len(notifications),
        "notifications": notifications
    }


@app.delete(
    "/notifications/{notification_id}",
    status_code=204,
    summary="Eliminar notificación",
    tags=["Notificaciones"],
    responses={
        204: {"description": "Notificación eliminada"},
        404: {"description": "Notificación no encontrada"}
    }
)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una notificación por su ID.
    """
    
    # Buscar y eliminar la notificación
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=404,
            detail=f"Notificación con ID {notification_id} no encontrada"
        )
    
    db.delete(notification)
    db.commit()
    
    return None
