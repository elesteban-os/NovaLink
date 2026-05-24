from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.database import Base


class Skill(Base):
    """Modelo SQLAlchemy para Skill."""
    
    __tablename__ = "skills"
    
    # Campos
    skill_id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(255), nullable=False, index=True)
    difficulty_level = Column(Integer, nullable=False, default=0)
    stock = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Skill(skill_id={self.skill_id}, skill_name='{self.skill_name}', difficulty={self.difficulty_level})>"
