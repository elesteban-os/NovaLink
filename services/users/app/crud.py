from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash


# USER CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: models.User, user_update: schemas.UserUpdate):
    update_data = user_update.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user

# SKILL DE USER CRUD xd
def get_user_skills(db: Session, user_id: int):
    return db.query(models.UserSkill.skill_name).filter(models.UserSkill.user_id == user_id).all()

def add_user_skill(db: Session, user_id: int, skill_name: str):
    # Check if skill already exists for this user to avoid duplicates
    existing_skill = db.query(models.UserSkill).filter(
        models.UserSkill.user_id == user_id, 
        models.UserSkill.skill_name == skill_name
    ).first()
    
    if existing_skill:
        return existing_skill
        
    db_skill = models.UserSkill(user_id=user_id, skill_name=skill_name)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill
