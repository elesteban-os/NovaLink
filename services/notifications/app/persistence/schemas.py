"""Pydantic schemas for notifications API request and response payloads."""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime


class NotificationCreate(BaseModel):
    """Schema for validating notification creation requests."""

    user_id: int = Field(..., gt=0, description="ID del usuario (debe ser positivo)")
    order_id: int = Field(..., gt=0, description="ID del pedido (debe ser positivo)")
    title: str = Field(
        ..., min_length=1, max_length=255, description="Título de la notificación"
    )
    description: str = Field(
        ..., min_length=1, description="Descripción de la notificación"
    )

    @field_validator("title")
    def title_not_empty(cls, v):
        """Ensure the notification title is not empty or whitespace only."""
        if not v.strip():
            raise ValueError("The title cannot be empty")
        return v.strip()

    @field_validator("description")
    def description_not_empty(cls, v):
        """Ensure the notification description is not empty or whitespace only."""
        if not v.strip():
            raise ValueError("The description cannot be empty")
        return v.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": 1,
                "order_id": 10,
                "title": "Habilidad adquirida",
                "description": "Has adquirido la habilidad de Empatía",
            }
        }
    )


class NotificationResponse(BaseModel):
    """Schema for serializing a single notification response."""

    id: int
    user_id: int
    order_id: int
    title: str
    description: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "order_id": 10,
                "title": "Habilidad adquirida",
                "description": "Has adquirido la habilidad de Empatía",
                "created_at": "2026-04-20T10:30:00",
            }
        },
    )


class NotificationListResponse(BaseModel):
    """Schema for paginated notification list responses."""

    total: int = Field(..., description="Total de notificaciones")
    count: int = Field(..., description="Cantidad de notificaciones en esta página")
    notifications: list[NotificationResponse]

    model_config = ConfigDict(
        json_schema_extra={
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
                        "created_at": "2026-04-20T10:30:00",
                    }
                ],
            }
        }
    )
