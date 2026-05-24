from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


# ===== USER SCHEMAS =====

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    
    email: EmailStr = Field(..., description="User email")
    first_name: str = Field(..., min_length=1, max_length=255, description="First name")
    last_name: str = Field(..., min_length=1, max_length=255, description="Last name")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    
    first_name: Optional[str] = Field(None, min_length=1, max_length=255)
    last_name: Optional[str] = Field(None, min_length=1, max_length=255)
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(BaseModel):
    """Schema for user response serialization."""
    
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
        """Extract skill names from ORM relationships or return passed list."""
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
    """Schema for user login requests."""
    
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="Password")


class Token(BaseModel):
    """Schema for JWT token response."""
    
    access_token: str
    token_type: str = "bearer"


# ===== USER SKILL SCHEMAS =====

class UserSkillCreate(BaseModel):
    """Schema for adding a skill to a user."""
    
    skill_name: str = Field(..., min_length=1, max_length=255)
    points: int = Field(default=1, ge=1)


class UserSkillResponse(BaseModel):
    """Schema for user skill response serialization."""
    
    id: int
    user_id: int
    skill_name: str
    points: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
