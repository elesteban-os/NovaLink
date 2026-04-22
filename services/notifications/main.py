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
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
