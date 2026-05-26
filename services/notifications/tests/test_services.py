from app.persistence.schemas import NotificationCreate
from app.services.notification_service import create_notification
from tests.test_utils import log_assert_equal, log_info


def test_create_notification_service(db_session):
    """Verifica que el servicio de notificaciones persiste el objeto y devuelve la entidad."""
    log_info(
        "[TEST] Ejecutando: test_create_notification_service -> crear notificación a través del servicio"
    )
    payload = NotificationCreate(
        user_id=1,
        order_id=10,
        title="Notificación servicio",
        description="Validación de servicio",
    )
    created = create_notification(db_session, notification_data=payload)

    log_assert_equal(True, created.id is not None, "created.id is not None")
    log_assert_equal(1, created.user_id, "created.user_id")
    log_assert_equal(10, created.order_id, "created.order_id")
    log_assert_equal("Notificación servicio", created.title, "created.title")


def test_create_notification_calls_email_send(monkeypatch, db_session):
    """Verifica que el servicio llame al envío de email simulado al crear la notificación."""
    log_info("[TEST] Ejecutando: test_create_notification_calls_email_send")

    sent = {"called": False, "notification_id": None}

    def fake_send_email(notification):
        sent["called"] = True
        sent["notification_id"] = notification.id
        return {"status": "sent"}

    from app.services import notification_service

    monkeypatch.setattr(notification_service, "send_email", fake_send_email)

    payload = NotificationCreate(
        user_id=2,
        order_id=20,
        title="Notificación de servicio mock",
        description="Prueba de llamada a send_email",
    )
    created = create_notification(db_session, notification_data=payload)

    log_assert_equal(True, sent["called"], "send_email fue llamado")
    log_assert_equal(
        created.id,
        sent["notification_id"],
        "send_email recibió la notificación correcta",
    )
