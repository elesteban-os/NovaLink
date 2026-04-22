from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relación con las skills
    skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")


class UserSkill(Base):
    __tablename__ = "user_skills"

    # Hacemos una llave primaria compuesta o simplemente un id autoincremental + unique constraint
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_name = Column(String, nullable=False)
    points = Column(Integer, default=1, nullable=False)

    user = relationship("User", back_populates="skills")
