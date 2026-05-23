from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...database import get_db
from ..persistence.schemas import NotificationCreate, NotificationResponse
from ..services.notification_service import create_notification as create_notification_service

router = APIRouter(tags=["Notificaciones"])


@router.post(
    "/notifications",
    response_model=NotificationResponse,
    status_code=201,
    summary="Crear nueva notificación",
    responses={
        201: {"description": "Notificación creada exitosamente"},
        422: {"description": "Validación fallida: user_id > 0, order_id > 0, title 1-255 caracteres, description no vacía"},
    },
)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
):
    return create_notification_service(db, notification)
