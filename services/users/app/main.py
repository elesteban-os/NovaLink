from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud, security
from .database import engine, get_db
from .seed_users import seed_users

# Crea la tablas de la DB
models.Base.metadata.create_all(bind=engine)

# Sembrar usuarios de prueba
seed_users()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Users Microservice")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# USER ENDPOINTS
@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users", response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.put("/users/{user_id}", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.update_user(db=db, db_user=db_user, user_update=user_update)

# SKILL ENDPOINTS
class UserSkillDetail(schemas.BaseModel):
    skill_name: str
    points: int

@app.get("/users/{user_id}/skills", response_model=List[UserSkillDetail])
def read_user_skills(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    skills = crud.get_user_skills(db=db, user_id=user_id)
    return [{"skill_name": skill.skill_name, "points": getattr(skill, "points", 1)} for skill in skills]

@app.post("/users/{user_id}/skills/{skill}", response_model=UserSkillDetail, status_code=status.HTTP_201_CREATED)
def add_skill_to_user(user_id: int, skill: str, quantity: int = 1, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    new_skill = crud.add_user_skill(db=db, user_id=user_id, skill_name=skill, quantity=quantity)
    return {"skill_name": new_skill.skill_name, "points": getattr(new_skill, "points", 1)}