import datetime
from sqlalchemy.orm import Session

from app.config import settings
from app.logger import logger
from app.persistence.crud import get_user_by_email
from app.persistence.schemas import Token, UserLogin
from app.security.auth import create_access_token, verify_password


class AuthService:
    """Authentication business logic for the Auth service."""

    def login(self, db: Session, user_credentials: UserLogin) -> Token | None:
        """Validate user credentials and return an access token for authorized users."""
        user = get_user_by_email(db, user_credentials.email)
        if not user:
            logger.warning("Login failed: user not found")
            return None

        if not verify_password(user_credentials.password, user.hashed_password):
            logger.warning("Login failed: invalid password")
            return None

        expires_delta = datetime.timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=expires_delta,
        )

        logger.info(f"Login successful for user: {user.email}")
        return Token(access_token=access_token, token_type="bearer")
