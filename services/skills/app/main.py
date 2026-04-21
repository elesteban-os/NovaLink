from typing import Generator, List, Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import engine
from app.db import SessionLocal
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class SkillCreate(BaseModel):
    skill_name: str
    difficulty_level: int
    stock: int


class SkillUpdate(BaseModel):
    skill_name: Optional[str] = None
    difficulty_level: Optional[int] = None
    stock: Optional[int] = None


class SkillResponse(BaseModel):
    skill_id: int
    skill_name: str
    difficulty_level: int
    stock: int

    class Config:
        from_attributes = True


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"msg": "API funcionando"}

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/skills", response_model=SkillResponse)
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    db_skill = models.Skill(
        skill_name=skill.skill_name,
        difficulty_level=skill.difficulty_level,
        stock=skill.stock,
    )
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@app.get("/skills", response_model=List[SkillResponse])
def list_skills(db: Session = Depends(get_db)):
    return db.query(models.Skill).all()


@app.get("/skills/{skill_id}", response_model=SkillResponse)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.skill_id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill no encontrada")

    return db_skill


@app.put("/skills/{skill_id}", response_model=SkillResponse)
def update_skill(skill_id: int, skill: SkillUpdate, db: Session = Depends(get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.skill_id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill no encontrada")

    if skill.skill_name is not None:
        db_skill.skill_name = skill.skill_name
    if skill.difficulty_level is not None:
        db_skill.difficulty_level = skill.difficulty_level
    if skill.stock is not None:
        db_skill.stock = skill.stock

    db.commit()
    db.refresh(db_skill)
    return db_skill


@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.skill_id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill no encontrada")

    db.delete(db_skill)
    db.commit()
    return {"message": "Skill eliminada correctamente"}