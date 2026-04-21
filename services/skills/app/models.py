from sqlalchemy import Column, Integer, String
from app.db import Base


class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String, nullable=False, index=True)
    difficulty_level = Column(Integer, nullable=False, default=0)
    stock = Column(Integer, nullable=False, default=0)
