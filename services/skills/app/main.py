from typing import Generator, List, Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db import engine
from app.db import SessionLocal
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Skills Service API",
    description="API para gestionar habilidades y stock.",
    version="1.0.0",
)


class ErrorResponse(BaseModel):
    detail: str


error_404_response = {
    "model": ErrorResponse,
    "description": "Recurso no encontrado.",
    "content": {
        "application/json": {
            "example": {"detail": "Skill no encontrada"}
        }
    },
}


class SkillCreate(BaseModel):
    skill_name: str = Field(..., min_length=1, max_length=100, description="Nombre de la habilidad")
    difficulty_level: int = Field(..., ge=0, le=10, description="Dificultad entre 0 y 10")
    stock: int = Field(..., ge=0, description="Stock disponible")


class SkillUpdate(BaseModel):
    skill_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre de la habilidad")
    difficulty_level: Optional[int] = Field(None, ge=0, le=10, description="Dificultad entre 0 y 10")
    stock: Optional[int] = Field(None, ge=0, description="Stock disponible")


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


@app.get("/", tags=["System"], summary="Estado base del servicio")
def root():
    return {"msg": "API funcionando"}


@app.get("/health", tags=["System"], summary="Health check")
def health():
    return {"status": "ok"}


@app.post(
    "/skills",
    response_model=SkillResponse,
    status_code=201,
    tags=["Skills"],
    summary="Crear una skill",
    responses={
        201: {"description": "Skill creada correctamente."},
        422: {"description": "Error de validacion en la solicitud."},
    },
)
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


@app.get(
    "/skills",
    response_model=List[SkillResponse],
    tags=["Skills"],
    summary="Listar skills",
    responses={
        200: {"description": "Listado de skills."},
    },
)
def list_skills(db: Session = Depends(get_db)):
    return db.query(models.Skill).all()


@app.get(
    "/skills/{skill_id}",
    response_model=SkillResponse,
    tags=["Skills"],
    summary="Obtener una skill por ID",
    responses={
        200: {"description": "Skill encontrada."},
        404: error_404_response,
        422: {"description": "Error de validacion en path params."},
    },
)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.skill_id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill no encontrada")

    return db_skill


@app.put(
    "/skills/{skill_id}",
    response_model=SkillResponse,
    tags=["Skills"],
    summary="Actualizar una skill por ID",
    responses={
        200: {"description": "Skill actualizada correctamente."},
        404: error_404_response,
        422: {"description": "Error de validacion en la solicitud."},
    },
)
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


@app.delete(
    "/skills/{skill_id}",
    tags=["Skills"],
    summary="Eliminar una skill por ID",
    responses={
        200: {
            "description": "Skill eliminada correctamente.",
            "content": {
                "application/json": {
                    "example": {"message": "Skill eliminada correctamente"}
                }
            },
        },
        404: error_404_response,
        422: {"description": "Error de validacion en path params."},
    },
)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.skill_id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill no encontrada")

    db.delete(db_skill)
    db.commit()
    return {"message": "Skill eliminada correctamente"}