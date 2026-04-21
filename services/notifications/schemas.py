"""
Esquemas Pydantic para validación de datos de entrada y serialización de respuestas.
Todos los atributos están en minúsculas.
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime


class NotificationCreate(BaseModel):
    """
    Esquema para crear una nueva notificación.
    Valida que los datos recibidos sean correctos.
    """
    
    user_id: int = Field(..., gt=0, description="ID del usuario (debe ser positivo)")
    order_id: int = Field(..., gt=0, description="ID del pedido (debe ser positivo)")
    title: str = Field(..., min_length=1, max_length=255, description="Título de la notificación")
    description: str = Field(..., min_length=1, description="Descripción de la notificación")

    @validator('title')
    def title_not_empty(cls, v):
        """Valida que el título no sea solo espacios en blanco."""
        if not v.strip():
            raise ValueError("El título no puede estar vacío")
        return v.strip()

    @validator('description')
    def description_not_empty(cls, v):
        """Valida que la descripción no sea solo espacios en blanco."""
        if not v.strip():
            raise ValueError("La descripción no puede estar vacía")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "order_id": 10,
                "title": "Habilidad adquirida",
                "description": "Has adquirido la habilidad de Empatía"
            }
        }


class NotificationResponse(BaseModel):
    """
    Esquema para la respuesta de una notificación.
    Se utiliza para serializar datos de la base de datos.
    """
    
    id: int
    user_id: int
    order_id: int
    title: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "order_id": 10,
                "title": "Habilidad adquirida",
                "description": "Has adquirido la habilidad de Empatía",
                "created_at": "2026-04-20T10:30:00"
            }
        }


class NotificationListResponse(BaseModel):
    """
    Esquema para la respuesta de lista de notificaciones con paginación.
    """
    
    total: int = Field(..., description="Total de notificaciones")
    count: int = Field(..., description="Cantidad de notificaciones en esta página")
    notifications: list[NotificationResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "total": 5,
                "count": 2,
                "notifications": [
                    {
                        "id": 1,
                        "user_id": 1,
                        "order_id": 10,
                        "title": "Habilidad adquirida",
                        "description": "Has adquirido la habilidad de Empatía",
                        "created_at": "2026-04-20T10:30:00"
                    }
                ]
            }
        }
