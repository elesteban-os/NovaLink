from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """Modelo de Usuario."""
    
    __tablename__ = "users"

    # Identificador
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos del usuario
    email = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relaciones
    skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"


class UserSkill(Base):
    """Modelo de Habilidad de Usuario (relación muchos-a-muchos)."""
    
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    skill_name = Column(String(255), nullable=False)
    points = Column(Integer, default=1, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relaciones
    user = relationship("User", back_populates="skills")
    
    def __repr__(self) -> str:
        return f"<UserSkill(user_id={self.user_id}, skill='{self.skill_name}', points={self.points})>"
