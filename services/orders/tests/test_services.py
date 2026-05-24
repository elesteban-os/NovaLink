import logging
import pytest
from pydantic import ValidationError

from app.persistence.schemas import OrderCreate
from app.services.order_service import create_order
from tests.test_utils import log_assert_equal, log_info


def test_create_order_service(db_session):
    """Verifica que el servicio crea la orden con los datos correctos."""
    log_info("[TEST] Ejecutando: test_create_order_service -> crear orden a través del servicio")
    order_data = OrderCreate(skill_name="SQLAlchemy", quantity=2)
    created = create_order(db_session, user_id=2, order_data=order_data)
    # Log and assert expected values
    log_assert_equal(True, created.id is not None, "created.id is not None")
    log_assert_equal(2, created.user_id, "created.user_id")
    log_assert_equal("SQLAlchemy", created.skill_name, "created.skill_name")
    log_assert_equal(2, created.quantity, "created.quantity")


def test_create_order_service_invalid_quantity_raises_validation_error():
    log_info("[TEST] Ejecutando: test_create_order_service_invalid_quantity_raises_validation_error -> cantidad inválida")
    with pytest.raises(ValidationError):
        OrderCreate(skill_name="SQLAlchemy", quantity=0)


def test_create_order_service_blank_skill_raises_validation_error():
    log_info("[TEST] Ejecutando: test_create_order_service_blank_skill_raises_validation_error -> skill vacío")
    with pytest.raises(ValidationError):
        OrderCreate(skill_name="   ", quantity=1)
