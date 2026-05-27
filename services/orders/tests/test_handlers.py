import logging

import pytest

logger = logging.getLogger(__name__)
from tests.test_utils import log_assert_equal, log_info


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_create_order_endpoint(client, auth_token):
    """Verifica que POST /orders crea una orden y devuelve el payload correcto."""
    logger.info("[TEST] Ejecutando: test_create_order_endpoint -> POST /orders")
    response = client.post(
        "/orders",
        json={"skill_name": "FastAPI", "quantity": 1},
        headers=_auth_headers(auth_token),
    )

    log_assert_equal(201, response.status_code, "status_code for POST /orders")
    data = response.json()
    log_assert_equal("FastAPI", data["skill_name"], "skill_name in response")
    log_assert_equal(1, data["quantity"], "quantity in response")
    log_assert_equal(1, data["user_id"], "user_id in response")
    log_info("[ASSERT] id exists in response: %r" % ("id" in data,))


def test_create_order_endpoint_missing_authorization(client):
    logger.info(
        "[TEST] Ejecutando: test_create_order_endpoint_missing_authorization -> sin Authorization header"
    )
    response = client.post(
        "/orders",
        json={"skill_name": "FastAPI", "quantity": 1},
    )

    log_assert_equal(
        401, response.status_code, "status_code when missing authorization"
    )
    log_assert_equal(
        "Missing or invalid token",
        response.json()["detail"],
        "error detail when missing authorization",
    )


def test_create_order_endpoint_invalid_token(client):
    logger.info(
        "[TEST] Ejecutando: test_create_order_endpoint_invalid_token -> token inválido"
    )
    response = client.post(
        "/orders",
        json={"skill_name": "FastAPI", "quantity": 1},
        headers={"Authorization": "Bearer bad.jwt.token"},
    )

    log_assert_equal(401, response.status_code, "status_code when token invalid")
    log_assert_equal(
        "Invalid token", response.json()["detail"], "error detail when token invalid"
    )


def test_create_order_endpoint_blank_skill_name_returns_422(client, auth_token):
    logger.info(
        "[TEST] Ejecutando: test_create_order_endpoint_blank_skill_name_returns_422 -> skill_name en blanco"
    )
    response = client.post(
        "/orders",
        json={"skill_name": "   ", "quantity": 1},
        headers=_auth_headers(auth_token),
    )

    log_assert_equal(422, response.status_code, "status_code when blank skill_name")
    errors = response.json()["detail"]
    assert any(error["loc"][-1] == "skill_name" for error in errors)


def test_create_order_endpoint_negative_quantity_returns_422(client, auth_token):
    logger.info(
        "[TEST] Ejecutando: test_create_order_endpoint_negative_quantity_returns_422 -> quantity <= 0"
    )
    response = client.post(
        "/orders",
        json={"skill_name": "FastAPI", "quantity": 0},
        headers=_auth_headers(auth_token),
    )

    log_assert_equal(422, response.status_code, "status_code when negative quantity")
    errors = response.json()["detail"]
    assert any(error["loc"][-1] == "quantity" for error in errors)
