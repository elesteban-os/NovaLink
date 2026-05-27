from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.persistence.crud import create_order
from app.persistence.models import Base, Order
from app.persistence.schemas import OrderCreate
from tests.test_utils import log_assert_equal, log_info


def test_create_order_crud(db_session):
    """Verifica que el CRUD persiste una orden en PostgreSQL."""
    log_info("[TEST] Ejecutando: test_create_order_crud -> crear orden usando CRUD")
    order_data = OrderCreate(skill_name="Testing", quantity=3)
    created = create_order(db_session, user_id=3, order_data=order_data)

    persisted = db_session.query(Order).filter_by(id=created.id).one()
    log_assert_equal("Testing", persisted.skill_name, "persisted.skill_name")
    log_assert_equal(3, persisted.user_id, "persisted.user_id")
    log_assert_equal(3, persisted.quantity, "persisted.quantity")


def test_create_order_persistence_in_memory():
    log_info(
        "[TEST] Ejecutando: test_create_order_persistence_in_memory -> persistencia en memoria"
    )
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        order_data = OrderCreate(skill_name="UnitTestOrder", quantity=4)
        created = create_order(session, user_id=7, order_data=order_data)

        persisted = session.query(Order).filter_by(id=created.id).one()
        log_assert_equal("UnitTestOrder", persisted.skill_name, "persisted.skill_name")
        log_assert_equal(7, persisted.user_id, "persisted.user_id")
        log_assert_equal(4, persisted.quantity, "persisted.quantity")
    finally:
        session.close()
