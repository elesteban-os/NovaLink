from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


# ===== USER SCHEMAS =====

class UserCreate(BaseModel):
    """Schema para creación de usuario."""
    
    email: EmailStr = Field(..., description="Email del usuario")
    first_name: str = Field(..., min_length=1, max_length=255, description="Nombre")
    last_name: str = Field(..., min_length=1, max_length=255, description="Apellido")
    password: str = Field(..., min_length=8, description="Contraseña (mínimo 8 caracteres)")


class UserUpdate(BaseModel):
    """Schema para actualización de usuario."""
    
    first_name: Optional[str] = Field(None, min_length=1, max_length=255)
    last_name: Optional[str] = Field(None, min_length=1, max_length=255)
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(BaseModel):
    """Schema para respuesta de usuario."""
    
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    skills: List[str] = []
    created_at: datetime
    updated_at: datetime
    
    @field_validator('skills', mode='before')
    @classmethod
    def extract_skills(cls, v):
        """Extraer nombres de skills del ORM."""
        if not v:
            return []
        # Si ya son strings
        if isinstance(v, list) and v and isinstance(v[0], str):
            return v
        # Si vienen del ORM
        if isinstance(v, list):
            return [skill.skill_name for skill in v]
        return []
    
    model_config = ConfigDict(from_attributes=True)


# ===== AUTH SCHEMAS =====

class UserLogin(BaseModel):
    """Schema para login de usuario."""
    
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña")


class Token(BaseModel):
    """Schema para respuesta de token."""
    
    access_token: str
    token_type: str = "bearer"


# ===== USER SKILL SCHEMAS =====

class UserSkillCreate(BaseModel):
    """Schema para agregar skill a usuario."""
    
    skill_name: str = Field(..., min_length=1, max_length=255)
    points: int = Field(default=1, ge=1)


class UserSkillResponse(BaseModel):
    """Schema para respuesta de user skill."""
    
    id: int
    user_id: int
    skill_name: str
    points: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
