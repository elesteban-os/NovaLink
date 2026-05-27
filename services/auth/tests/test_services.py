"""Tests for the auth service layer (business logic)."""

import pytest
import logging
from datetime import datetime, timedelta

from app.persistence.schemas import UserLogin, Token
from app.services.auth_service import AuthService
from app.config import settings
from tests.test_utils import log_assert_equal, log_info

logger = logging.getLogger(__name__)


# ===== LOGIN SERVICE TESTS =====

def test_login_service_with_valid_credentials(db_session, test_user):
    """Verifies that AuthService.login returns a token for valid credentials."""
    log_info("[TEST] Ejecutando: test_login_service_with_valid_credentials")
    
    service = AuthService()
    user_credentials = UserLogin(email="test@example.com", password="testpassword123")
    
    token = service.login(db_session, user_credentials)
    
    log_assert_equal(True, token is not None, "token is not None")
    log_assert_equal(True, hasattr(token, "access_token"), "token has access_token")
    log_assert_equal("bearer", token.token_type, "token_type is 'bearer'")


def test_login_service_with_invalid_password(db_session, test_user):
    """Verifies that AuthService.login returns None for invalid password."""
    log_info("[TEST] Ejecutando: test_login_service_with_invalid_password")
    
    service = AuthService()
    user_credentials = UserLogin(email="test@example.com", password="wrongpassword")
    
    token = service.login(db_session, user_credentials)
    
    log_assert_equal(None, token, "token is None for invalid password")


def test_login_service_with_nonexistent_user(db_session):
    """Verifies that AuthService.login returns None for non-existent user."""
    log_info("[TEST] Ejecutando: test_login_service_with_nonexistent_user")
    
    service = AuthService()
    user_credentials = UserLogin(email="nonexistent@example.com", password="password123")
    
    token = service.login(db_session, user_credentials)
    
    log_assert_equal(None, token, "token is None for non-existent user")


def test_login_service_generates_valid_token_format(db_session, test_user):
    """Verifies that the generated token is a valid JWT format."""
    log_info("[TEST] Ejecutando: test_login_service_generates_valid_token_format")
    
    service = AuthService()
    user_credentials = UserLogin(email="test@example.com", password="testpassword123")
    
    token = service.login(db_session, user_credentials)
    
    # JWT token should have 3 parts separated by dots
    parts = token.access_token.split(".")
    log_assert_equal(3, len(parts), "JWT token has 3 parts")


def test_login_service_preserves_user_context(db_session, test_user):
    """Verifies that the token contains user email and ID in claims."""
    log_info("[TEST] Ejecutando: test_login_service_preserves_user_context")
    
    import jwt
    
    service = AuthService()
    user_credentials = UserLogin(email="test@example.com", password="testpassword123")
    
    token = service.login(db_session, user_credentials)
    
    # Decode token to verify claims
    decoded = jwt.decode(
        token.access_token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM]
    )
    
    log_assert_equal("test@example.com", decoded.get("sub"), "token contains user email in 'sub' claim")
    log_assert_equal(True, "user_id" in decoded, "token contains user_id claim")
