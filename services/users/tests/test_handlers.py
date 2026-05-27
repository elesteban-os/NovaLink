"""Tests for the users API handlers (HTTP endpoints)."""

import logging
import pytest

logger = logging.getLogger(__name__)
from tests.test_utils import log_assert_equal, log_info


# ===== CREATE USER ENDPOINT TESTS =====


def test_create_user_endpoint(client, db_session):
    """Verifies that POST /users creates a user and returns the payload correctly."""
    log_info("[TEST] Ejecutando: test_create_user_endpoint -> POST /users")

    response = client.post(
        "/users",
        json={
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "securepassword123",
        },
    )

    log_assert_equal(201, response.status_code, "status_code for POST /users")
    data = response.json()
    log_assert_equal("newuser@example.com", data["email"], "email in response")
    log_assert_equal("New", data["first_name"], "first_name in response")
    log_assert_equal("User", data["last_name"], "last_name in response")
    log_assert_equal(True, data["is_active"], "is_active in response")
    log_assert_equal(True, "id" in data, "id exists in response")


def test_create_user_endpoint_duplicate_email(client, db_session):
    """Verifies that creating a user with duplicate email returns 400."""
    log_info("[TEST] Ejecutando: test_create_user_endpoint_duplicate_email")

    user_data = {
        "email": "duplicate@example.com",
        "first_name": "First",
        "last_name": "User",
        "password": "password123",
    }

    # First request succeeds
    response1 = client.post("/users", json=user_data)
    log_assert_equal(201, response1.status_code, "first user creation returns 201")

    # Second request with same email fails
    response2 = client.post("/users", json=user_data)
    log_assert_equal(400, response2.status_code, "duplicate email returns 400")


def test_create_user_endpoint_invalid_email(client):
    """Verifies that invalid email format returns 422."""
    log_info("[TEST] Ejecutando: test_create_user_endpoint_invalid_email")

    response = client.post(
        "/users",
        json={
            "email": "invalid-email",
            "first_name": "Invalid",
            "last_name": "Email",
            "password": "password123",
        },
    )

    log_assert_equal(422, response.status_code, "invalid email returns 422")


def test_create_user_endpoint_short_password(client):
    """Verifies that password shorter than 8 characters returns 422."""
    log_info("[TEST] Ejecutando: test_create_user_endpoint_short_password")

    response = client.post(
        "/users",
        json={
            "email": "user@example.com",
            "first_name": "Short",
            "last_name": "Pass",
            "password": "short",
        },
    )

    log_assert_equal(422, response.status_code, "short password returns 422")


# ===== GET USERS ENDPOINT TESTS =====


def test_list_users_endpoint(client, db_session):
    """Verifies that GET /users returns a list of users."""
    log_info("[TEST] Ejecutando: test_list_users_endpoint -> GET /users")

    response = client.get("/users")

    log_assert_equal(200, response.status_code, "status_code for GET /users")
    data = response.json()
    log_assert_equal(True, isinstance(data, list), "response is a list")


def test_list_users_endpoint_with_pagination(client, db_session):
    """Verifies that GET /users respects skip and limit parameters."""
    log_info("[TEST] Ejecutando: test_list_users_endpoint_with_pagination")

    response = client.get("/users?skip=0&limit=10")

    log_assert_equal(
        200, response.status_code, "status_code for GET /users with pagination"
    )
    data = response.json()
    log_assert_equal(True, isinstance(data, list), "response is a list")


# ===== GET USER BY ID ENDPOINT TESTS =====


def test_get_user_by_id_endpoint(client, db_session):
    """Verifies that GET /users/{id} returns a user."""
    log_info("[TEST] Ejecutando: test_get_user_by_id_endpoint -> GET /users/{id}")

    # Create a user first
    create_response = client.post(
        "/users",
        json={
            "email": "getbyid@example.com",
            "first_name": "Get",
            "last_name": "ById",
            "password": "password123",
        },
    )
    created_user = create_response.json()
    user_id = created_user["id"]

    # Get the user
    response = client.get(f"/users/{user_id}")

    log_assert_equal(200, response.status_code, "status_code for GET /users/{id}")
    data = response.json()
    log_assert_equal(user_id, data["id"], "id matches")
    log_assert_equal("getbyid@example.com", data["email"], "email matches")


def test_get_nonexistent_user_by_id(client):
    """Verifies that GET /users/{id} returns 404 for non-existent user."""
    log_info("[TEST] Ejecutando: test_get_nonexistent_user_by_id")

    response = client.get("/users/99999")

    log_assert_equal(
        404, response.status_code, "status_code for non-existent user is 404"
    )


# ===== UPDATE USER ENDPOINT TESTS =====


def test_update_user_endpoint(client, db_session):
    """Verifies that PUT /users/{id} updates a user."""
    log_info("[TEST] Ejecutando: test_update_user_endpoint -> PUT /users/{id}")

    # Create a user first
    create_response = client.post(
        "/users",
        json={
            "email": "update@example.com",
            "first_name": "Old",
            "last_name": "Name",
            "password": "password123",
        },
    )
    created_user = create_response.json()
    user_id = created_user["id"]

    # Update the user
    response = client.put(
        f"/users/{user_id}", json={"first_name": "New", "last_name": "Updated"}
    )

    log_assert_equal(200, response.status_code, "status_code for PUT /users/{id}")
    data = response.json()
    log_assert_equal("New", data["first_name"], "first_name updated")
    log_assert_equal("Updated", data["last_name"], "last_name updated")


def test_update_nonexistent_user(client):
    """Verifies that PUT /users/{id} returns 404 for non-existent user."""
    log_info("[TEST] Ejecutando: test_update_nonexistent_user")

    response = client.put("/users/99999", json={"first_name": "New"})

    log_assert_equal(
        404, response.status_code, "status_code for non-existent user is 404"
    )


# ===== DELETE USER ENDPOINT TESTS =====


def test_delete_user_endpoint(client, db_session):
    """Verifies that DELETE /users/{id} deletes a user."""
    log_info("[TEST] Ejecutando: test_delete_user_endpoint -> DELETE /users/{id}")

    # Create a user first
    create_response = client.post(
        "/users",
        json={
            "email": "delete@example.com",
            "first_name": "Delete",
            "last_name": "Me",
            "password": "password123",
        },
    )
    created_user = create_response.json()
    user_id = created_user["id"]

    # Delete the user
    response = client.delete(f"/users/{user_id}")

    log_assert_equal(204, response.status_code, "status_code for DELETE /users/{id}")


def test_delete_nonexistent_user(client):
    """Verifies that DELETE /users/{id} returns 404 for non-existent user."""
    log_info("[TEST] Ejecutando: test_delete_nonexistent_user")

    response = client.delete("/users/99999")

    log_assert_equal(
        404, response.status_code, "status_code for non-existent user is 404"
    )


# ===== ADD USER SKILL ENDPOINT TESTS =====


def test_add_user_skill_endpoint(client, db_session):
    """Verifies that POST /users/{id}/skills adds a skill to a user."""
    log_info(
        "[TEST] Ejecutando: test_add_user_skill_endpoint -> POST /users/{id}/skills"
    )

    # Create a user first
    create_response = client.post(
        "/users",
        json={
            "email": "skilluser@example.com",
            "first_name": "Skill",
            "last_name": "User",
            "password": "password123",
        },
    )
    created_user = create_response.json()
    user_id = created_user["id"]

    # Add a skill
    response = client.post(
        f"/users/{user_id}/skills", json={"skill_name": "Python", "points": 10}
    )

    log_assert_equal(
        201, response.status_code, "status_code for POST /users/{id}/skills"
    )
    data = response.json()
    log_assert_equal("Python", data["skill_name"], "skill_name in response")
    log_assert_equal(10, data["points"], "points in response")


def test_add_skill_to_nonexistent_user(client):
    """Verifies that POST /users/{id}/skills returns 404 for non-existent user."""
    log_info("[TEST] Ejecutando: test_add_skill_to_nonexistent_user")

    response = client.post(
        "/users/99999/skills", json={"skill_name": "Python", "points": 10}
    )

    log_assert_equal(
        404, response.status_code, "status_code for non-existent user is 404"
    )


# ===== GET USER SKILLS ENDPOINT TESTS =====


def test_get_user_skills_endpoint(client, db_session):
    """Verifies that GET /users/{id}/skills returns user skills."""
    log_info(
        "[TEST] Ejecutando: test_get_user_skills_endpoint -> GET /users/{id}/skills"
    )

    # Create a user
    create_response = client.post(
        "/users",
        json={
            "email": "getskills@example.com",
            "first_name": "Get",
            "last_name": "Skills",
            "password": "password123",
        },
    )
    created_user = create_response.json()
    user_id = created_user["id"]

    # Add skills
    for skill in ["Python", "FastAPI", "React"]:
        client.post(f"/users/{user_id}/skills", json={"skill_name": skill, "points": 5})

    # Get skills
    response = client.get(f"/users/{user_id}/skills")

    log_assert_equal(
        200, response.status_code, "status_code for GET /users/{id}/skills"
    )
    data = response.json()
    log_assert_equal(3, len(data), "response contains 3 skills")


def test_get_skills_for_nonexistent_user(client):
    """Verifies that GET /users/{id}/skills returns 404 for non-existent user."""
    log_info("[TEST] Ejecutando: test_get_skills_for_nonexistent_user")

    response = client.get("/users/99999/skills")

    log_assert_equal(
        404, response.status_code, "status_code for non-existent user is 404"
    )


# ===== REMOVE USER SKILL ENDPOINT TESTS =====


def test_remove_user_skill_endpoint(client, db_session):
    """Verifies that DELETE /users/{id}/skills/{name} removes a skill."""
    log_info(
        "[TEST] Ejecutando: test_remove_user_skill_endpoint -> DELETE /users/{id}/skills/{name}"
    )

    # Create a user
    create_response = client.post(
        "/users",
        json={
            "email": "removeskill@example.com",
            "first_name": "Remove",
            "last_name": "Skill",
            "password": "password123",
        },
    )
    created_user = create_response.json()
    user_id = created_user["id"]

    # Add a skill
    client.post(
        f"/users/{user_id}/skills", json={"skill_name": "Kubernetes", "points": 8}
    )

    # Remove the skill
    response = client.delete(f"/users/{user_id}/skills/Kubernetes")

    log_assert_equal(
        204, response.status_code, "status_code for DELETE /users/{id}/skills/{name}"
    )


def test_remove_nonexistent_skill(client, db_session):
    """Verifies that DELETE /users/{id}/skills/{name} returns 404 for non-existent skill."""
    log_info("[TEST] Ejecutando: test_remove_nonexistent_skill")

    # Create a user
    create_response = client.post(
        "/users",
        json={
            "email": "removenonskill@example.com",
            "first_name": "Remove",
            "last_name": "NoSkill",
            "password": "password123",
        },
    )
    created_user = create_response.json()
    user_id = created_user["id"]

    # Try to remove non-existent skill
    response = client.delete(f"/users/{user_id}/skills/NonExistent")

    log_assert_equal(
        404, response.status_code, "status_code for non-existent skill is 404"
    )


# ===== HEALTH CHECK ENDPOINT TEST =====


def test_health_endpoint(client):
    """Verifies that GET /health returns ok status."""
    log_info("[TEST] Ejecutando: test_health_endpoint -> GET /health")

    response = client.get("/health")

    log_assert_equal(200, response.status_code, "status_code for GET /health")
    data = response.json()
    log_assert_equal("ok", data["status"], "health status is ok")
