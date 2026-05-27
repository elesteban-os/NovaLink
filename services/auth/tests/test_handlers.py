"""Tests for the auth API handlers (HTTP endpoints)."""

import logging
import pytest

logger = logging.getLogger(__name__)
from tests.test_utils import log_assert_equal, log_info


# ===== LOGIN ENDPOINT TESTS =====


def test_login_endpoint_with_valid_credentials(client, db_session, test_user):
    """Verifies that POST /auth/login returns a token for valid credentials."""
    log_info(
        "[TEST] Ejecutando: test_login_endpoint_with_valid_credentials -> POST /auth/login"
    )

    response = client.post(
        "/auth/login", json={"email": "test@example.com", "password": "testpassword123"}
    )

    log_assert_equal(
        200,
        response.status_code,
        "status_code for POST /auth/login with valid credentials",
    )
    data = response.json()
    log_assert_equal(True, "access_token" in data, "access_token in response")
    log_assert_equal("bearer", data["token_type"], "token_type is 'bearer'")


def test_login_endpoint_with_invalid_password(client, db_session, test_user):
    """Verifies that POST /auth/login returns 401 for invalid password."""
    log_info("[TEST] Ejecutando: test_login_endpoint_with_invalid_password")

    response = client.post(
        "/auth/login", json={"email": "test@example.com", "password": "wrongpassword"}
    )

    log_assert_equal(
        401, response.status_code, "status_code for invalid password is 401"
    )
    data = response.json()
    log_assert_equal(
        "Incorrect email or password",
        data["detail"],
        "detail message for invalid password",
    )


def test_login_endpoint_with_nonexistent_user(client):
    """Verifies that POST /auth/login returns 401 for non-existent user."""
    log_info("[TEST] Ejecutando: test_login_endpoint_with_nonexistent_user")

    response = client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "password123"},
    )

    log_assert_equal(
        401, response.status_code, "status_code for non-existent user is 401"
    )
    data = response.json()
    log_assert_equal(
        "Incorrect email or password",
        data["detail"],
        "detail message for non-existent user",
    )


def test_login_endpoint_with_missing_email(client):
    """Verifies that POST /auth/login returns 422 when email is missing."""
    log_info("[TEST] Ejecutando: test_login_endpoint_with_missing_email")

    response = client.post("/auth/login", json={"password": "password123"})

    log_assert_equal(422, response.status_code, "status_code for missing email is 422")


def test_login_endpoint_with_missing_password(client):
    """Verifies that POST /auth/login returns 422 when password is missing."""
    log_info("[TEST] Ejecutando: test_login_endpoint_with_missing_password")

    response = client.post("/auth/login", json={"email": "test@example.com"})

    log_assert_equal(
        422, response.status_code, "status_code for missing password is 422"
    )


def test_login_endpoint_with_invalid_email_format(client):
    """Verifies that POST /auth/login returns 422 for invalid email format."""
    log_info("[TEST] Ejecutando: test_login_endpoint_with_invalid_email_format")

    response = client.post(
        "/auth/login", json={"email": "invalid-email", "password": "password123"}
    )

    log_assert_equal(
        422, response.status_code, "status_code for invalid email format is 422"
    )


def test_login_endpoint_returns_valid_jwt(client, db_session, test_user):
    """Verifies that the returned token is a valid JWT."""
    log_info("[TEST] Ejecutando: test_login_endpoint_returns_valid_jwt")

    response = client.post(
        "/auth/login", json={"email": "test@example.com", "password": "testpassword123"}
    )

    log_assert_equal(200, response.status_code, "login successful")
    data = response.json()

    # JWT should have 3 parts separated by dots
    token_parts = data["access_token"].split(".")
    log_assert_equal(3, len(token_parts), "JWT token has 3 parts")


# ===== HEALTH CHECK ENDPOINT TEST =====


def test_health_endpoint(client):
    """Verifies that GET /health returns ok status."""
    log_info("[TEST] Ejecutando: test_health_endpoint -> GET /health")

    response = client.get("/health")

    log_assert_equal(200, response.status_code, "status_code for GET /health")
    data = response.json()
    log_assert_equal("ok", data["status"], "health status is ok")


# ===== ROOT ENDPOINT TEST =====


def test_root_endpoint(client):
    """Verifies that GET / returns a running message."""
    log_info("[TEST] Ejecutando: test_root_endpoint -> GET /")

    response = client.get("/")

    log_assert_equal(200, response.status_code, "status_code for GET /")
    data = response.json()
    log_assert_equal(True, "message" in data, "message in response")
