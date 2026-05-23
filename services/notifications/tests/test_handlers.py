from tests.test_utils import log_assert_equal, log_info


def test_create_notification_endpoint(client):
    """Verifica que POST /notifications crea una notificación correctamente."""
    log_info("[TEST] Ejecutando: test_create_notification_endpoint -> POST /notifications")
    payload = {
        "user_id": 1,
        "order_id": 10,
        "title": "Notificación de prueba",
        "description": "Descripción de prueba",
    }
    response = client.post("/notifications", json=payload)

    log_assert_equal(201, response.status_code, "status_code for POST /notifications")
    data = response.json()
    log_assert_equal(1, data["user_id"], "user_id in response")
    log_assert_equal(10, data["order_id"], "order_id in response")
    log_assert_equal("Notificación de prueba", data["title"], "title in response")
    log_info("[ASSERT] id exists in response: %r" % ("id" in data,))
