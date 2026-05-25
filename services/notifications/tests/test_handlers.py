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


def test_create_notification_invalid_payload_returns_422(client):
    """Verifica que un payload inválido genere un 422 de validación."""
    log_info("[TEST] Ejecutando: test_create_notification_invalid_payload_returns_422")
    payload = {
        "user_id": 0,
        "order_id": -1,
        "title": "   ",
        "description": "   ",
    }
    response = client.post("/notifications", json=payload)

    log_assert_equal(422, response.status_code, "status_code for invalid payload")
    data = response.json()
    log_assert_equal(True, "detail" in data, "response contains detail")
