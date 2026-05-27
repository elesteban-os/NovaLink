from app.persistence.crud import create_notification
from app.persistence.models import Notification
from app.persistence.schemas import NotificationCreate
from tests.test_utils import log_assert_equal, log_info


def test_create_notification_crud(db_session):
    """Verifica que el CRUD persiste la notificación en PostgreSQL."""
    log_info(
        "[TEST] Ejecutando: test_create_notification_crud -> crear notificación usando CRUD"
    )
    payload = NotificationCreate(
        user_id=1,
        order_id=10,
        title="Persistencia",
        description="Verifica persistencia en base de datos",
    )
    created = create_notification(db_session, notification_data=payload)

    persisted = db_session.query(Notification).filter_by(id=created.id).one()
    log_assert_equal("Persistencia", persisted.title, "persisted.title")
    log_assert_equal(
        "Verifica persistencia en base de datos",
        persisted.description,
        "persisted.description",
    )
