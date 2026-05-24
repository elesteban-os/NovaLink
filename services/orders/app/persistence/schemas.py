"""Pydantic schemas for request and response models in the orders service."""

from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from typing import Optional

class OrderCreate(BaseModel):
    """Payload schema for creating an order."""
    model_config = ConfigDict()

    skill_name: str = Field(..., min_length=1, max_length=255, description="Nombre de la habilidad (FK)")
    quantity: int = Field(..., gt=0, description="Cantidad solicitada (debe ser > 0)")
    
    @field_validator('skill_name')
    @classmethod
    def no_whitespace_only(cls, v):
        if not v.strip():
            raise ValueError("skill_name no puede estar solo de espacios en blanco")
        return v.strip()

class OrderResponse(BaseModel):
    """Response schema for order details."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    skill_name: str
    quantity: int
    issued_by: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderListResponse(BaseModel):
    """Response schema for a list of orders with pagination metadata."""
    model_config = ConfigDict()

    total: int
    count: int
    orders: list[OrderResponse]
