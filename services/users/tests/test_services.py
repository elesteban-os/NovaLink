"""Tests for the users service layer (business logic)."""

import pytest
import logging

from app.persistence.schemas import UserCreate, UserUpdate, UserSkillCreate
from app.services.user_service import user_service
from tests.test_utils import log_assert_equal, log_info

logger = logging.getLogger(__name__)


# ===== CREATE USER SERVICE TESTS =====

def test_create_user_service(db_session):
    """Verifies that user_service.create_user creates and returns a user."""
    log_info("[TEST] Ejecutando: test_create_user_service -> crear usuario a través del servicio")
    
    user_data = UserCreate(
        email="service@example.com",
        first_name="Service",
        last_name="User",
        password="password123"
    )
    
    created = user_service.create_user(db_session, user_data)
    
    log_assert_equal(True, created.id is not None, "created.id is not None")
    log_assert_equal("service@example.com", created.email, "created.email")
    log_assert_equal("Service", created.first_name, "created.first_name")


def test_create_user_service_duplicate_email_raises_error(db_session):
    """Verifies that creating a user with duplicate email raises ValueError."""
    log_info("[TEST] Ejecutando: test_create_user_service_duplicate_email_raises_error")
    
    user_data_1 = UserCreate(
        email="duplicate@example.com",
        first_name="First",
        last_name="User",
        password="password123"
    )
    user_service.create_user(db_session, user_data_1)
    
    user_data_2 = UserCreate(
        email="duplicate@example.com",
        first_name="Second",
        last_name="User",
        password="password456"
    )
    
    with pytest.raises(ValueError) as exc_info:
        user_service.create_user(db_session, user_data_2)
    
    log_assert_equal("Email already registered", str(exc_info.value), "error message for duplicate email")


# ===== GET USER SERVICE TESTS =====

def test_get_user_service(db_session):
    """Verifies that user_service.get_user retrieves a user by ID."""
    log_info("[TEST] Ejecutando: test_get_user_service")
    
    user_data = UserCreate(
        email="getservice@example.com",
        first_name="Get",
        last_name="Service",
        password="password123"
    )
    created = user_service.create_user(db_session, user_data)
    
    retrieved = user_service.get_user(db_session, created.id)
    
    log_assert_equal(created.id, retrieved.id, "retrieved.id matches created.id")


def test_get_user_service_not_found_raises_error(db_session):
    """Verifies that getting a non-existent user raises ValueError."""
    log_info("[TEST] Ejecutando: test_get_user_service_not_found_raises_error")
    
    with pytest.raises(ValueError) as exc_info:
        user_service.get_user(db_session, 99999)
    
    log_assert_equal("User not found", str(exc_info.value), "error message for not found")


# ===== GET USERS SERVICE TESTS =====

def test_get_users_service(db_session):
    """Verifies that user_service.get_users returns a list of users."""
    log_info("[TEST] Ejecutando: test_get_users_service")
    
    # Create multiple users
    for i in range(3):
        user_data = UserCreate(
            email=f"serviceuser{i}@example.com",
            first_name=f"Service{i}",
            last_name="User",
            password="password123"
        )
        user_service.create_user(db_session, user_data)
    
    users = user_service.get_users(db_session, skip=0, limit=10)
    
    log_assert_equal(True, len(users) >= 3, "get_users returns at least 3 users")


# ===== UPDATE USER SERVICE TESTS =====

def test_update_user_service(db_session):
    """Verifies that user_service.update_user modifies user data."""
    log_info("[TEST] Ejecutando: test_update_user_service")
    
    user_data = UserCreate(
        email="updateservice@example.com",
        first_name="Old",
        last_name="Name",
        password="password123"
    )
    created = user_service.create_user(db_session, user_data)
    
    update_data = UserUpdate(first_name="New", last_name="Updated")
    updated = user_service.update_user(db_session, created.id, update_data)
    
    log_assert_equal("New", updated.first_name, "updated.first_name is 'New'")
    log_assert_equal("Updated", updated.last_name, "updated.last_name is 'Updated'")


def test_update_nonexistent_user_raises_error(db_session):
    """Verifies that updating a non-existent user raises ValueError."""
    log_info("[TEST] Ejecutando: test_update_nonexistent_user_raises_error")
    
    update_data = UserUpdate(first_name="New")
    
    with pytest.raises(ValueError) as exc_info:
        user_service.update_user(db_session, 99999, update_data)
    
    log_assert_equal("User not found", str(exc_info.value), "error message for not found")


# ===== DELETE USER SERVICE TESTS =====

def test_delete_user_service(db_session):
    """Verifies that user_service.delete_user deactivates a user."""
    log_info("[TEST] Ejecutando: test_delete_user_service")
    
    user_data = UserCreate(
        email="deleteservice@example.com",
        first_name="Delete",
        last_name="Me",
        password="password123"
    )
    created = user_service.create_user(db_session, user_data)
    user_id = created.id
    
    user_service.delete_user(db_session, user_id)
    
    # Verify user is deactivated
    user = user_service.get_user(db_session, user_id)
    log_assert_equal(False, user.is_active, "user.is_active is False after deletion")


def test_delete_nonexistent_user_service_raises_error(db_session):
    """Verifies that deleting a non-existent user raises ValueError."""
    log_info("[TEST] Ejecutando: test_delete_nonexistent_user_service_raises_error")
    
    with pytest.raises(ValueError) as exc_info:
        user_service.delete_user(db_session, 99999)
    
    log_assert_equal("User not found", str(exc_info.value), "error message for not found")


# ===== ADD USER SKILL SERVICE TESTS =====

def test_add_user_skill_service(db_session):
    """Verifies that user_service.add_user_skill adds a skill to a user."""
    log_info("[TEST] Ejecutando: test_add_user_skill_service")
    
    # Create user
    user_data = UserCreate(
        email="skillservice@example.com",
        first_name="Skill",
        last_name="User",
        password="password123"
    )
    user = user_service.create_user(db_session, user_data)
    
    # Add skill
    skill_data = UserSkillCreate(skill_name="Python", points=10)
    skill = user_service.add_user_skill(db_session, user.id, skill_data)
    
    log_assert_equal("Python", skill.skill_name, "skill.skill_name is 'Python'")
    log_assert_equal(10, skill.points, "skill.points is 10")


def test_add_skill_to_nonexistent_user_raises_error(db_session):
    """Verifies that adding a skill to non-existent user raises ValueError."""
    log_info("[TEST] Ejecutando: test_add_skill_to_nonexistent_user_raises_error")
    
    skill_data = UserSkillCreate(skill_name="Python", points=10)
    
    with pytest.raises(ValueError) as exc_info:
        user_service.add_user_skill(db_session, 99999, skill_data)
    
    log_assert_equal("User not found", str(exc_info.value), "error message for not found")


# ===== GET USER SKILLS SERVICE TESTS =====

def test_get_user_skills_service(db_session):
    """Verifies that user_service.get_user_skills returns all skills for a user."""
    log_info("[TEST] Ejecutando: test_get_user_skills_service")
    
    # Create user
    user_data = UserCreate(
        email="getskillservice@example.com",
        first_name="Get",
        last_name="Skills",
        password="password123"
    )
    user = user_service.create_user(db_session, user_data)
    
    # Add skills
    for skill_name in ["FastAPI", "React", "Docker"]:
        skill_data = UserSkillCreate(skill_name=skill_name, points=5)
        user_service.add_user_skill(db_session, user.id, skill_data)
    
    skills = user_service.get_user_skills(db_session, user.id)
    
    log_assert_equal(3, len(skills), "user should have 3 skills")


def test_get_skills_for_nonexistent_user_raises_error(db_session):
    """Verifies that getting skills for non-existent user raises ValueError."""
    log_info("[TEST] Ejecutando: test_get_skills_for_nonexistent_user_raises_error")
    
    with pytest.raises(ValueError) as exc_info:
        user_service.get_user_skills(db_session, 99999)
    
    log_assert_equal("User not found", str(exc_info.value), "error message for not found")


# ===== REMOVE USER SKILL SERVICE TESTS =====

def test_remove_user_skill_service(db_session):
    """Verifies that user_service.remove_user_skill removes a skill from a user."""
    log_info("[TEST] Ejecutando: test_remove_user_skill_service")
    
    # Create user and add skill
    user_data = UserCreate(
        email="removeskillservice@example.com",
        first_name="Remove",
        last_name="Skill",
        password="password123"
    )
    user = user_service.create_user(db_session, user_data)
    
    skill_data = UserSkillCreate(skill_name="Kubernetes", points=8)
    user_service.add_user_skill(db_session, user.id, skill_data)
    
    # Remove skill
    user_service.remove_user_skill(db_session, user.id, "Kubernetes")
    
    # Verify skill is removed
    skills = user_service.get_user_skills(db_session, user.id)
    log_assert_equal(0, len(skills), "user should have 0 skills")


def test_remove_nonexistent_skill_from_service_raises_error(db_session):
    """Verifies that removing non-existent skill raises ValueError."""
    log_info("[TEST] Ejecutando: test_remove_nonexistent_skill_from_service_raises_error")
    
    # Create user
    user_data = UserCreate(
        email="removefailservice@example.com",
        first_name="Remove",
        last_name="Fail",
        password="password123"
    )
    user = user_service.create_user(db_session, user_data)
    
    with pytest.raises(ValueError) as exc_info:
        user_service.remove_user_skill(db_session, user.id, "NonExistent")
    
    log_assert_equal("Skill not found", str(exc_info.value), "error message for not found")


def test_remove_skill_from_nonexistent_user_raises_error(db_session):
    """Verifies that removing skill from non-existent user raises ValueError."""
    log_info("[TEST] Ejecutando: test_remove_skill_from_nonexistent_user_raises_error")
    
    with pytest.raises(ValueError) as exc_info:
        user_service.remove_user_skill(db_session, 99999, "SomeSkill")
    
    log_assert_equal("User not found", str(exc_info.value), "error message for not found")
