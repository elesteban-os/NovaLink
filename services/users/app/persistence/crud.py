from sqlalchemy.orm import Session
from typing import List, Optional

from app.persistence.models import User, UserSkill
from app.persistence.schemas import UserCreate, UserUpdate, UserSkillCreate
from app.security.auth import get_password_hash
from app.logger import logger


# ===== USER CRUD =====

def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Crear nuevo usuario en BD.
    
    Args:
        db: Sesión de BD
        user_data: Datos a crear
        
    Returns:
        Usuario creado
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
    logger.info(f"Usuario creado: {db_user.id} ({db_user.email})")
    return db_user


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Obtener usuario por ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Obtener usuario por email."""
    return db.query(User).filter(User.email == email).first()


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = True
) -> List[User]:
    """
    Listar usuarios con paginación.
    
    Args:
        db: Sesión de BD
        skip: Saltar registros
        limit: Límite de registros
        is_active: Filtrar por estado (None = todos)
        
    Returns:
        Lista de usuarios
    """
    query = db.query(User)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()


def update_user(db: Session, db_user: User, user_data: UserUpdate) -> User:
    """
    Actualizar usuario.
    
    Args:
        db: Sesión de BD
        db_user: Instancia del usuario
        user_data: Datos de actualización
        
    Returns:
        Usuario actualizado
    """
    update_data = user_data.model_dump(exclude_unset=True)
    
    # Hash de password si se proporciona
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Usuario actualizado: {db_user.id}")
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """
    Eliminar usuario (soft delete).
    
    Args:
        db: Sesión de BD
        user_id: ID del usuario
        
    Returns:
        True si fue eliminado, False si no existe
    """
    db_user = get_user(db, user_id)
    
    if not db_user:
        logger.warning(f"Usuario no encontrado: {user_id}")
        return False
    
    db_user.is_active = False
    db.add(db_user)
    db.commit()
    logger.info(f"Usuario desactivado: {user_id}")
    return True


# ===== USER SKILL CRUD =====

def get_user_skills(db: Session, user_id: int) -> List[UserSkill]:
    """Obtener todas las skills de un usuario."""
    return db.query(UserSkill).filter(UserSkill.user_id == user_id).all()


def add_user_skill(
    db: Session,
    user_id: int,
    skill_data: UserSkillCreate
) -> UserSkill:
    """
    Agregar skill a usuario (o incrementar puntos si ya existe).
    
    Args:
        db: Sesión de BD
        user_id: ID del usuario
        skill_data: Datos del skill
        
    Returns:
        User skill creado o actualizado
    """
    # Verificar si el skill ya existe
    existing_skill = db.query(UserSkill).filter(
        UserSkill.user_id == user_id,
        UserSkill.skill_name == skill_data.skill_name
    ).first()
    
    if existing_skill:
        logger.info(f"Skill ya existe para usuario {user_id}, incrementando puntos")
        existing_skill.points += skill_data.points
        db.add(existing_skill)
        db.commit()
        db.refresh(existing_skill)
        return existing_skill
        
    # Crear nuevo skill
    db_skill = UserSkill(
        user_id=user_id,
        skill_name=skill_data.skill_name,
        points=skill_data.points
    )
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    logger.info(f"Skill agregado a usuario {user_id}: {skill_data.skill_name}")
    return db_skill


def remove_user_skill(db: Session, user_id: int, skill_name: str) -> bool:
    """
    Remover skill de usuario.
    
    Args:
        db: Sesión de BD
        user_id: ID del usuario
        skill_name: Nombre del skill
        
    Returns:
        True si fue removido, False si no existe
    """
    db_skill = db.query(UserSkill).filter(
        UserSkill.user_id == user_id,
        UserSkill.skill_name == skill_name
    ).first()
    
    if not db_skill:
        logger.warning(f"Skill no encontrado para usuario {user_id}: {skill_name}")
        return False
    
    db.delete(db_skill)
    db.commit()
    logger.info(f"Skill removido de usuario {user_id}: {skill_name}")
    return True
