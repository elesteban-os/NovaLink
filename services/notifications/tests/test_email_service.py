from app.email_service import send_email
from app.persistence.models import Notification


def test_send_email_simulation_returns_expected_dict():
    notification = Notification(
        id=1,
        user_id=1,
        order_id=10,
        title="Notificación prueba",
        description="Mensaje de notificación de prueba",
    )

    result = send_email(notification)

    assert result["status"] == "sent"
    assert result["notification_id"] == 1
    assert result["user_id"] == 1
    assert result["order_id"] == 10
    assert result["title"] == "Notificación prueba"
    assert result["simulated"] is True
    assert "timestamp" in result
