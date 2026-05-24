"""Persistence layer CRUD operations for users and user skills.

This module implements low-level DB operations used by the service layer.
Functions follow a simple contract: receive a `Session` and domain data,
perform DB actions, commit/refresh and return ORM objects or booleans.
"""

from sqlalchemy.orm import Session
from typing import List, Optional

from app.persistence.models import User, UserSkill
from app.persistence.schemas import UserCreate, UserUpdate, UserSkillCreate
from app.security.auth import get_password_hash
from app.logger import logger


# ===== USER CRUD =====

def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user record in the database.

    Args:
        db: Database session
        user_data: Data used to create the user

    Returns:
        The created User ORM instance
    """
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created: {db_user.id} ({db_user.email})")
    return db_user


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Return a user by its ID or None if not found."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Return a user by email address or None if not found."""
    return db.query(User).filter(User.email == email).first()


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = True
) -> List[User]:
    """List users with pagination and optional active-state filter.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        is_active: Filter by active state (None = all)

    Returns:
        List of User ORM instances
    """
    query = db.query(User)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()


def update_user(db: Session, db_user: User, user_data: UserUpdate) -> User:
    """Update an existing user instance with the provided data.

    Args:
        db: Database session
        db_user: User ORM instance to update
        user_data: Fields to update

    Returns:
        The updated User ORM instance
    """
    update_data = user_data.model_dump(exclude_unset=True)
    
    # Hash password if provided
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User updated: {db_user.id}")
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Soft-delete a user by marking it inactive.

    Args:
        db: Database session
        user_id: ID of the user to deactivate

    Returns:
        True if deactivated, False if user not found
    """
    db_user = get_user(db, user_id)
    
    if not db_user:
        logger.warning(f"User not found: {user_id}")
        return False
    
    db_user.is_active = False
    db.add(db_user)
    db.commit()
    logger.info(f"User deactivated: {user_id}")
    return True


# ===== USER SKILL CRUD =====

def get_user_skills(db: Session, user_id: int) -> List[UserSkill]:
    """Return all skills associated with a given user."""
    return db.query(UserSkill).filter(UserSkill.user_id == user_id).all()


def add_user_skill(
    db: Session,
    user_id: int,
    skill_data: UserSkillCreate
) -> UserSkill:
    """Add a skill to a user or increment points if the skill exists."""
    # Verificar si el skill ya existe
    existing_skill = db.query(UserSkill).filter(
        UserSkill.user_id == user_id,
        UserSkill.skill_name == skill_data.skill_name
    ).first()
    
    if existing_skill:
        logger.info(f"Skill already exists for user {user_id}, incrementing points")
        existing_skill.points += skill_data.points
        db.add(existing_skill)
        db.commit()
        db.refresh(existing_skill)
        return existing_skill
        
    # Create new skill
    db_skill = UserSkill(
        user_id=user_id,
        skill_name=skill_data.skill_name,
        points=skill_data.points
    )
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    logger.info(f"Skill added to user {user_id}: {skill_data.skill_name}")
    return db_skill


def remove_user_skill(db: Session, user_id: int, skill_name: str) -> bool:
    """Remove a skill from a user.

    Args:
        db: Database session
        user_id: ID of the user
        skill_name: Name of the skill to remove

    Returns:
        True if removed, False if not found
    """
    db_skill = db.query(UserSkill).filter(
        UserSkill.user_id == user_id,
        UserSkill.skill_name == skill_name
    ).first()
    
    if not db_skill:
        logger.warning(f"Skill not found for user {user_id}: {skill_name}")
        return False
    
    db.delete(db_skill)
    db.commit()
    logger.info(f"Skill removed from user {user_id}: {skill_name}")
    return True
