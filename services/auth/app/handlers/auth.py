"""Auth router definitions.

This module exposes the login endpoint and delegates credential validation
and token creation to the AuthService.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger import logger
from app.persistence.schemas import Token, UserLogin
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
service = AuthService()


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)) -> Token:
    """Authenticate the user and return a JWT token on success."""
    token = service.login(db, user_credentials)
    if not token:
        logger.warning("Unauthorized login attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
