from sqlalchemy.orm import Session
from typing import List, Optional

from app.persistence.models import Skill
from app.persistence.schemas import SkillCreate, SkillUpdate
from app.logger import logger


def create_skill(db: Session, obj_in: SkillCreate) -> Skill:
    """
    Crear nuevo skill en BD.
    
    Args:
        db: Sesión de BD
        obj_in: Datos a crear
        
    Returns:
        Objeto Skill creado
    """
    db_obj = Skill(**obj_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    logger.info(f"Skill creado: {db_obj.skill_id} - {db_obj.skill_name}")
    return db_obj


def get_skill(db: Session, skill_id: int) -> Optional[Skill]:
    """Obtener skill por ID."""
    return db.query(Skill).filter(Skill.skill_id == skill_id).first()


def get_skills(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = True
) -> List[Skill]:
    """
    Listar skills con paginación.
    
    Args:
        db: Sesión de BD
        skip: Número de registros a saltar
        limit: Número máximo de registros
        is_active: Filtrar por estado (None = todos)
        
    Returns:
        Lista de skills
    """
    query = db.query(Skill)
    
    if is_active is not None:
        query = query.filter(Skill.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()


def update_skill(
    db: Session,
    db_obj: Skill,
    obj_in: SkillUpdate
) -> Skill:
    """
    Actualizar skill.
    
    Args:
        db: Sesión de BD
        db_obj: Objeto a actualizar
        obj_in: Datos de actualización
        
    Returns:
        Objeto Skill actualizado
    """
    update_data = obj_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    logger.info(f"Skill actualizado: {db_obj.skill_id}")
    return db_obj


def delete_skill(db: Session, skill_id: int) -> bool:
    """
    Eliminar skill.
    
    Args:
        db: Sesión de BD
        skill_id: ID del skill
        
    Returns:
        True si fue eliminado, False si no existe
    """
    db_obj = get_skill(db, skill_id)
    
    if not db_obj:
        logger.warning(f"Skill no encontrado: {skill_id}")
        return False
    
    db.delete(db_obj)
    db.commit()
    logger.info(f"Skill eliminado: {skill_id}")
    return True
