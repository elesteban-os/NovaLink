from sqlalchemy.orm import Session
from typing import List, Optional

from app.persistence import crud
from app.persistence.models import Skill
from app.persistence.schemas import SkillCreate, SkillUpdate
from app.logger import logger


class SkillService:
    """Servicio de lógica de negocio para skills."""
    
    def create_skill(self, db: Session, obj_in: SkillCreate) -> Skill:
        """
        Crear nuevo skill con validaciones de negocio.
        
        Args:
            db: Sesión de BD
            obj_in: Datos a crear
            
        Returns:
            Skill creado
            
        Raises:
            ValueError: Si hay validación fallida
        """
        # Validar que no exista duplicado
        existing = db.query(Skill).filter(
            Skill.skill_name.ilike(obj_in.skill_name)
        ).first()
        
        if existing:
            logger.warning(f"Intento de crear skill duplicado: {obj_in.skill_name}")
            raise ValueError(f"Skill '{obj_in.skill_name}' ya existe")
        
        logger.info(f"Creando nuevo skill: {obj_in.skill_name}")
        return crud.create_skill(db, obj_in)
    
    def get_skill(self, db: Session, skill_id: int) -> Skill:
        """
        Obtener skill con validación.
        
        Raises:
            ValueError: Si el skill no existe
        """
        db_obj = crud.get_skill(db, skill_id)
        
        if not db_obj:
            logger.error(f"Skill no encontrado: {skill_id}")
            raise ValueError(f"Skill {skill_id} no encontrado")
        
        return db_obj
    
    def get_skills(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Skill]:
        """Listar skills."""
        return crud.get_skills(db, skip=skip, limit=limit)
    
    def update_skill(
        self,
        db: Session,
        skill_id: int,
        obj_in: SkillUpdate
    ) -> Skill:
        """
        Actualizar skill.
        
        Raises:
            ValueError: Si el skill no existe
        """
        db_obj = self.get_skill(db, skill_id)
        logger.info(f"Actualizando skill: {skill_id}")
        return crud.update_skill(db, db_obj, obj_in)
    
    def delete_skill(self, db: Session, skill_id: int) -> bool:
        """
        Eliminar skill.
        
        Returns:
            True si fue eliminado
            
        Raises:
            ValueError: Si el skill no existe
        """
        self.get_skill(db, skill_id)  # Validar existencia
        logger.info(f"Eliminando skill: {skill_id}")
        return crud.delete_skill(db, skill_id)
