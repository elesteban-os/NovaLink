from pydantic import BaseModel, EmailStr, field_validator
from typing import List

# SCHEMA SKILL
class SkillBase(BaseModel):
    skill_name: str

class SkillCreate(SkillBase):
    pass

class SkillResponse(BaseModel):
    # Ya no devolvemos el objeto entero, vamos a devolver directamente List[str] en los endpoints
    pass

#Auth / Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# USER SCHEMAS
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None

class UserResponse(UserBase):
    id: int
    skills: List[str] = []

    @field_validator('skills', mode='before')
    @classmethod
    def extract_skills(cls, v):
        if not v:
            return []
        # Si ya son strings (por ejemplo desde una lista normal)
        if isinstance(v[0], str):
            return v
        # Si vienen del ORM (modelos de SQLAlchemy)
        return [skill.skill_name for skill in v]

    class Config:
        from_attributes = True
