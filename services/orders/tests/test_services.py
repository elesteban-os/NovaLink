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


def test_create_order_service_publishes_event(monkeypatch, db_session):
    log_info("[TEST] Ejecutando: test_create_order_service_publishes_event -> evento de orden publicado")

    published = {}

    def fake_publish_event(routing_key, payload):
        published["called"] = True
        published["routing_key"] = routing_key
        published["payload"] = payload

    monkeypatch.setattr("app.services.order_service.publish_event", fake_publish_event)

    order_data = OrderCreate(skill_name="UnitTestSkill", quantity=5)
    created = create_order(db_session, user_id=10, order_data=order_data)

    log_assert_equal(True, published.get("called", False), "publish_event called")
    log_assert_equal("pedido.creado", published.get("routing_key"), "routing_key for created order event")
    log_assert_equal(10, published["payload"]["user_id"], "user_id in published event")
    log_assert_equal(created.id, published["payload"]["pedido_id"], "pedido_id in published event")
    log_assert_equal("UnitTestSkill", published["payload"]["skill_name"], "skill_name in published event")


def test_create_order_service_invalid_quantity_raises_validation_error():
    log_info("[TEST] Ejecutando: test_create_order_service_invalid_quantity_raises_validation_error -> cantidad inválida")
    with pytest.raises(ValidationError):
        OrderCreate(skill_name="SQLAlchemy", quantity=0)


def test_create_order_service_blank_skill_raises_validation_error():
    log_info("[TEST] Ejecutando: test_create_order_service_blank_skill_raises_validation_error -> skill vacío")
    with pytest.raises(ValidationError):
        OrderCreate(skill_name="   ", quantity=1)
