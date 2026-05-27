"""Business logic (service layer) for users.

Responsibilities:
- Validate input and existence checks
- Coordinate persistence calls in `app.persistence.crud`
- Log business events
"""

from typing import List

from sqlalchemy.orm import Session

from app.logger import logger
from app.persistence import crud
from app.persistence.models import User, UserSkill
from app.persistence.schemas import UserCreate, UserSkillCreate, UserUpdate


class UserService:
    """Business layer for user operations.

    Responsibilities:
    - Validate input and existence checks
    - Coordinate persistence calls in `app.persistence.crud`
    - Log business events
    """

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        if crud.get_user_by_email(db, user_data.email):
            logger.warning(
                f"Attempt to create user with existing email: {user_data.email}"
            )
            raise ValueError("Email already registered")

        user = crud.create_user(db, user_data)
        logger.info(f"User created successfully: {user.id}")
        return user

    def get_user(self, db: Session, user_id: int) -> User:
        user = crud.get_user(db, user_id)
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise ValueError("User not found")
        return user

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return crud.get_users(db, skip=skip, limit=limit)

    def update_user(self, db: Session, user_id: int, user_data: UserUpdate) -> User:
        user = crud.get_user(db, user_id)
        if not user:
            logger.warning(f"Attempt to update non-existent user: {user_id}")
            raise ValueError("User not found")
        updated_user = crud.update_user(db, user, user_data)
        logger.info(f"User updated successfully: {user_id}")
        return updated_user

    def delete_user(self, db: Session, user_id: int) -> None:
        if not crud.delete_user(db, user_id):
            logger.warning(f"Attempt to delete non-existent user: {user_id}")
            raise ValueError("User not found")
        logger.info(f"User deactivated successfully: {user_id}")

    def add_user_skill(
        self, db: Session, user_id: int, skill_data: UserSkillCreate
    ) -> UserSkill:
        user = crud.get_user(db, user_id)
        if not user:
            logger.warning(f"Attempt to add skill to non-existent user: {user_id}")
            raise ValueError("User not found")

        skill = crud.add_user_skill(db, user_id, skill_data)
        logger.info(f"Skill '{skill.skill_name}' added to user {user_id}")
        return skill

    def get_user_skills(self, db: Session, user_id: int) -> List[UserSkill]:
        user = crud.get_user(db, user_id)
        if not user:
            logger.warning(f"Attempt to list skills for non-existent user: {user_id}")
            raise ValueError("User not found")
        return crud.get_user_skills(db, user_id)

    def remove_user_skill(self, db: Session, user_id: int, skill_name: str) -> None:
        user = crud.get_user(db, user_id)
        if not user:
            logger.warning(f"Attempt to remove skill from non-existent user: {user_id}")
            raise ValueError("User not found")

        if not crud.remove_user_skill(db, user_id, skill_name):
            logger.warning(f"Skill not found for user {user_id}: {skill_name}")
            raise ValueError("Skill not found")
        logger.info(f"Skill '{skill_name}' removed from user {user_id}")


user_service = UserService()
