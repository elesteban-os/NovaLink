def test_post_skill_creates_skill(client):
    payload = {
        "skill_name": "prueba_unitaria_skill",
        "difficulty_level": 3,
        "stock": 100,
    }

    response = client.post("/skills", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["skill_name"] == "prueba_unitaria_skill"
    assert body["difficulty_level"] == 3
    assert body["stock"] == 100
    assert body["is_active"] is True


def test_get_skills_returns_list(client):
    payload = {"skill_name": "habilidad_de_prueba", "difficulty_level": 2, "stock": 50}
    create_resp = client.post("/skills", json=payload)
    assert create_resp.status_code == 201

    response = client.get("/skills")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert any(item["skill_name"] == "habilidad_de_prueba" for item in body)


def test_get_skill_not_found_returns_404(client):
    response = client.get("/skills/999999")

    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"].lower()


def test_post_skill_validation_returns_422(client):
    response = client.post(
        "/skills", json={"skill_name": "", "difficulty_level": -1, "stock": -5}
    )

    assert response.status_code == 422
    body = response.json()
    assert body["detail"]
