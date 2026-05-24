"""HTTP handlers (routers) for the users service.

Template for this service:
- Endpoint input: POST/GET/PUT/DELETE `/users` and skill endpoints under `/users/{id}/skills`.
- Business logic: validate and delegate to `user_service`.
- Endpoint output: `UserResponse` or `UserSkillResponse` DTOs, or appropriate HTTP codes.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger import logger
from app.persistence.schemas import (
    UserCreate,
    UserResponse,
    UserSkillCreate,
    UserSkillResponse,
    UserUpdate,
)
from app.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    try:
        return user_service.create_user(db, user)
    except ValueError as exc:
        logger.warning(f"Create user failed: {exc}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        logger.error(f"Unexpected error creating user: {exc}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[UserResponse]:
    return user_service.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    try:
        return user_service.get_user(db, user_id)
    except ValueError as exc:
        logger.warning(f"Get user failed: {exc}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)) -> UserResponse:
    try:
        return user_service.update_user(db, user_id, user_update)
    except ValueError as exc:
        logger.warning(f"Update user failed: {exc}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        logger.error(f"Unexpected error updating user: {exc}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    try:
        user_service.delete_user(db, user_id)
    except ValueError as exc:
        logger.warning(f"Delete user failed: {exc}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/{user_id}/skills", response_model=UserSkillResponse, status_code=status.HTTP_201_CREATED)
def add_user_skill(user_id: int, skill_data: UserSkillCreate, db: Session = Depends(get_db)) -> UserSkillResponse:
    try:
        return user_service.add_user_skill(db, user_id, skill_data)
    except ValueError as exc:
        logger.warning(f"Add skill failed: {exc}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        logger.error(f"Unexpected error adding skill: {exc}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{user_id}/skills", response_model=List[UserSkillResponse], status_code=status.HTTP_200_OK)
def list_user_skills(user_id: int, db: Session = Depends(get_db)) -> List[UserSkillResponse]:
    try:
        return user_service.get_user_skills(db, user_id)
    except ValueError as exc:
        logger.warning(f"List user skills failed: {exc}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{user_id}/skills/{skill_name}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user_skill(user_id: int, skill_name: str, db: Session = Depends(get_db)) -> None:
    try:
        user_service.remove_user_skill(db, user_id, skill_name)
    except ValueError as exc:
        logger.warning(f"Remove user skill failed: {exc}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
