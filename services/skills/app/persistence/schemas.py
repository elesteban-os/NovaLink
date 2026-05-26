"""Pydantic schemas for skill request and response models."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SkillCreate(BaseModel):
    """Schema para creación de skill."""

    skill_name: str = Field(
        ..., min_length=1, max_length=255, description="Nombre de la habilidad"
    )
    difficulty_level: int = Field(
        ..., ge=0, le=10, description="Dificultad entre 0 y 10"
    )
    stock: int = Field(..., ge=0, description="Stock disponible")


class SkillUpdate(BaseModel):
    """Schema para actualización de skill."""

    skill_name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Nombre de la habilidad"
    )
    difficulty_level: Optional[int] = Field(
        None, ge=0, le=10, description="Dificultad entre 0 y 10"
    )
    stock: Optional[int] = Field(None, ge=0, description="Stock disponible")
    is_active: Optional[bool] = None


class SkillResponse(BaseModel):
    """Schema para respuesta de skill."""

    skill_id: int
    skill_name: str
    difficulty_level: int
    stock: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
