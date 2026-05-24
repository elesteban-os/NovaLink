from typing import List

from sqlalchemy.orm import Session

from app.logger import logger
from app.persistence import crud
from app.persistence.models import User, UserSkill
from app.persistence.schemas import UserCreate, UserSkillCreate, UserUpdate


class UserService:
    """Capa de negocio para operaciones de usuario."""

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        if crud.get_user_by_email(db, user_data.email):
            logger.warning(f"Intento de crear usuario con email existente: {user_data.email}")
            raise ValueError("Email already registered")

        user = crud.create_user(db, user_data)
        logger.info(f"Usuario creado correctamente: {user.id}")
        return user

    def get_user(self, db: Session, user_id: int) -> User:
        user = crud.get_user(db, user_id)
        if not user:
            logger.warning(f"Usuario no encontrado: {user_id}")
            raise ValueError("User not found")
        return user

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return crud.get_users(db, skip=skip, limit=limit)

    def update_user(self, db: Session, user_id: int, user_data: UserUpdate) -> User:
        user = crud.get_user(db, user_id)
        if not user:
            logger.warning(f"Intento de actualizar usuario inexistente: {user_id}")
            raise ValueError("User not found")
        updated_user = crud.update_user(db, user, user_data)
        logger.info(f"Usuario actualizado correctamente: {user_id}")
        return updated_user

    def delete_user(self, db: Session, user_id: int) -> None:
        if not crud.delete_user(db, user_id):
            logger.warning(f"Intento de eliminar usuario inexistente: {user_id}")
            raise ValueError("User not found")
        logger.info(f"Usuario desactivado correctamente: {user_id}")

    def add_user_skill(self, db: Session, user_id: int, skill_data: UserSkillCreate) -> UserSkill:
        user = crud.get_user(db, user_id)
        if not user:
            logger.warning(f"Intento de agregar skill a usuario inexistente: {user_id}")
            raise ValueError("User not found")

        skill = crud.add_user_skill(db, user_id, skill_data)
        logger.info(f"Skill '{skill.skill_name}' agregada al usuario {user_id}")
        return skill

    def get_user_skills(self, db: Session, user_id: int) -> List[UserSkill]:
        user = crud.get_user(db, user_id)
        if not user:
            logger.warning(f"Intento de listar skills de usuario inexistente: {user_id}")
            raise ValueError("User not found")
        return crud.get_user_skills(db, user_id)

    def remove_user_skill(self, db: Session, user_id: int, skill_name: str) -> None:
        user = crud.get_user(db, user_id)
        if not user:
            logger.warning(f"Intento de remover skill de usuario inexistente: {user_id}")
            raise ValueError("User not found")

        if not crud.remove_user_skill(db, user_id, skill_name):
            logger.warning(f"Skill no encontrada para usuario {user_id}: {skill_name}")
            raise ValueError("Skill not found")
        logger.info(f"Skill '{skill_name}' removida del usuario {user_id}")


user_service = UserService()
