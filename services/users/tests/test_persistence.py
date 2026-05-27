"""Tests for the users persistence layer (CRUD operations)."""

import pytest
import logging

from app.persistence.schemas import UserCreate, UserUpdate, UserSkillCreate
from app.persistence import crud
from tests.test_utils import log_assert_equal, log_info

logger = logging.getLogger(__name__)


# ===== CREATE USER TESTS =====

def test_create_user_persistence(db_session):
    """Verifies that create_user persists the user object and returns the created entity."""
    log_info("[TEST] Ejecutando: test_create_user_persistence -> crear usuario en base de datos")
    
    user_data = UserCreate(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        password="securepassword123"
    )
    
    created = crud.create_user(db_session, user_data)
    
    log_assert_equal(True, created.id is not None, "created.id is not None")
    log_assert_equal("test@example.com", created.email, "created.email")
    log_assert_equal("John", created.first_name, "created.first_name")
    log_assert_equal("Doe", created.last_name, "created.last_name")
    log_assert_equal(True, created.is_active, "created.is_active")


def test_create_user_with_duplicate_email(db_session):
    """Verifies that creating users with duplicate emails results in database error."""
    log_info("[TEST] Ejecutando: test_create_user_with_duplicate_email")
    
    user_data_1 = UserCreate(
        email="duplicate@example.com",
        first_name="John",
        last_name="Doe",
        password="password123"
    )
    
    # First creation should succeed
    crud.create_user(db_session, user_data_1)
    
    # Second creation with same email should raise an exception
    user_data_2 = UserCreate(
        email="duplicate@example.com",
        first_name="Jane",
        last_name="Doe",
        password="password456"
    )
    
    with pytest.raises(Exception):
        crud.create_user(db_session, user_data_2)


# ===== GET USER TESTS =====

def test_get_user_by_id(db_session):
    """Verifies that get_user retrieves user by ID."""
    log_info("[TEST] Ejecutando: test_get_user_by_id -> obtener usuario por ID")
    
    user_data = UserCreate(
        email="getuser@example.com",
        first_name="Alice",
        last_name="Smith",
        password="password789"
    )
    created = crud.create_user(db_session, user_data)
    
    retrieved = crud.get_user(db_session, created.id)
    
    log_assert_equal(created.id, retrieved.id, "retrieved.id matches created.id")
    log_assert_equal(created.email, retrieved.email, "retrieved.email matches created.email")


def test_get_user_nonexistent(db_session):
    """Verifies that get_user returns None for non-existent user."""
    log_info("[TEST] Ejecutando: test_get_user_nonexistent")
    
    result = crud.get_user(db_session, 99999)
    
    log_assert_equal(None, result, "get_user returns None for non-existent ID")


def test_get_user_by_email(db_session):
    """Verifies that get_user_by_email retrieves user by email."""
    log_info("[TEST] Ejecutando: test_get_user_by_email")
    
    user_data = UserCreate(
        email="byemail@example.com",
        first_name="Bob",
        last_name="Johnson",
        password="passwordabc"
    )
    created = crud.create_user(db_session, user_data)
    
    retrieved = crud.get_user_by_email(db_session, "byemail@example.com")
    
    log_assert_equal(created.id, retrieved.id, "retrieved.id matches created.id")
    log_assert_equal("byemail@example.com", retrieved.email, "retrieved.email matches")


def test_get_user_by_email_nonexistent(db_session):
    """Verifies that get_user_by_email returns None for non-existent email."""
    log_info("[TEST] Ejecutando: test_get_user_by_email_nonexistent")
    
    result = crud.get_user_by_email(db_session, "nonexistent@example.com")
    
    log_assert_equal(None, result, "get_user_by_email returns None for non-existent email")


# ===== GET USERS TESTS =====

def test_get_users_empty(db_session):
    """Verifies that get_users returns empty list when no users exist."""
    log_info("[TEST] Ejecutando: test_get_users_empty")
    
    users = crud.get_users(db_session)
    
    log_assert_equal(0, len(users), "get_users returns empty list")


def test_get_users_with_pagination(db_session):
    """Verifies that get_users respects skip and limit parameters."""
    log_info("[TEST] Ejecutando: test_get_users_with_pagination")
    
    # Create 5 users
    for i in range(5):
        user_data = UserCreate(
            email=f"user{i}@example.com",
            first_name=f"User{i}",
            last_name="Test",
            password="password123"
        )
        crud.create_user(db_session, user_data)
    
    # Test pagination
    users = crud.get_users(db_session, skip=2, limit=2)
    
    log_assert_equal(2, len(users), "get_users returns 2 users with limit=2")


def test_get_users_active_filter(db_session):
    """Verifies that get_users filters by is_active status."""
    log_info("[TEST] Ejecutando: test_get_users_active_filter")
    
    # Create an active user
    user_data = UserCreate(
        email="active@example.com",
        first_name="Active",
        last_name="User",
        password="password123"
    )
    created = crud.create_user(db_session, user_data)
    
    # Get only active users
    active_users = crud.get_users(db_session, is_active=True)
    
    log_assert_equal(True, len(active_users) > 0, "get_users returns active users")


# ===== UPDATE USER TESTS =====

def test_update_user_first_name(db_session):
    """Verifies that update_user changes the first name."""
    log_info("[TEST] Ejecutando: test_update_user_first_name")
    
    user_data = UserCreate(
        email="update@example.com",
        first_name="Old",
        last_name="Name",
        password="password123"
    )
    created = crud.create_user(db_session, user_data)
    
    update_data = UserUpdate(first_name="New")
    updated = crud.update_user(db_session, created, update_data)
    
    log_assert_equal("New", updated.first_name, "updated.first_name is 'New'")
    log_assert_equal("Name", updated.last_name, "updated.last_name remains 'Name'")


def test_update_user_password(db_session):
    """Verifies that update_user can change the password."""
    log_info("[TEST] Ejecutando: test_update_user_password")
    
    user_data = UserCreate(
        email="updatepass@example.com",
        first_name="Pass",
        last_name="Update",
        password="oldpassword123"
    )
    created = crud.create_user(db_session, user_data)
    old_hash = created.hashed_password
    
    update_data = UserUpdate(password="newpassword456")
    updated = crud.update_user(db_session, created, update_data)
    
    log_assert_equal(True, updated.hashed_password != old_hash, "hashed_password changed")


# ===== DELETE USER TESTS =====

def test_delete_user_soft_delete(db_session):
    """Verifies that delete_user marks user as inactive."""
    log_info("[TEST] Ejecutando: test_delete_user_soft_delete")
    
    user_data = UserCreate(
        email="delete@example.com",
        first_name="Delete",
        last_name="Me",
        password="password123"
    )
    created = crud.create_user(db_session, user_data)
    user_id = created.id
    
    result = crud.delete_user(db_session, user_id)
    
    log_assert_equal(True, result, "delete_user returns True on success")
    
    # Verify the user is marked inactive
    user = crud.get_user(db_session, user_id)
    log_assert_equal(False, user.is_active, "user.is_active is False after deletion")


def test_delete_nonexistent_user(db_session):
    """Verifies that delete_user returns False for non-existent user."""
    log_info("[TEST] Ejecutando: test_delete_nonexistent_user")
    
    result = crud.delete_user(db_session, 99999)
    
    log_assert_equal(False, result, "delete_user returns False for non-existent user")


# ===== USER SKILL TESTS =====

def test_add_user_skill(db_session):
    """Verifies that add_user_skill adds a skill to a user."""
    log_info("[TEST] Ejecutando: test_add_user_skill")
    
    # Create a user first
    user_data = UserCreate(
        email="skilluser@example.com",
        first_name="Skill",
        last_name="User",
        password="password123"
    )
    user = crud.create_user(db_session, user_data)
    
    # Add a skill
    skill_data = UserSkillCreate(skill_name="Python", points=10)
    skill = crud.add_user_skill(db_session, user.id, skill_data)
    
    log_assert_equal(user.id, skill.user_id, "skill.user_id matches user.id")
    log_assert_equal("Python", skill.skill_name, "skill.skill_name is 'Python'")
    log_assert_equal(10, skill.points, "skill.points is 10")


def test_add_duplicate_user_skill_increments_points(db_session):
    """Verifies that adding the same skill twice increments points."""
    log_info("[TEST] Ejecutando: test_add_duplicate_user_skill_increments_points")
    
    # Create user
    user_data = UserCreate(
        email="dupskill@example.com",
        first_name="Dup",
        last_name="Skill",
        password="password123"
    )
    user = crud.create_user(db_session, user_data)
    
    # Add skill twice
    skill_data_1 = UserSkillCreate(skill_name="JavaScript", points=5)
    skill_1 = crud.add_user_skill(db_session, user.id, skill_data_1)
    
    skill_data_2 = UserSkillCreate(skill_name="JavaScript", points=3)
    skill_2 = crud.add_user_skill(db_session, user.id, skill_data_2)
    
    log_assert_equal(skill_1.id, skill_2.id, "same skill should have same ID")
    log_assert_equal(8, skill_2.points, "points should be 8 (5 + 3)")


def test_get_user_skills(db_session):
    """Verifies that get_user_skills returns all skills for a user."""
    log_info("[TEST] Ejecutando: test_get_user_skills")
    
    # Create user
    user_data = UserCreate(
        email="getskills@example.com",
        first_name="Get",
        last_name="Skills",
        password="password123"
    )
    user = crud.create_user(db_session, user_data)
    
    # Add multiple skills
    skills_data = [
        UserSkillCreate(skill_name="FastAPI", points=7),
        UserSkillCreate(skill_name="React", points=6),
        UserSkillCreate(skill_name="Docker", points=5)
    ]
    
    for skill_data in skills_data:
        crud.add_user_skill(db_session, user.id, skill_data)
    
    retrieved_skills = crud.get_user_skills(db_session, user.id)
    
    log_assert_equal(3, len(retrieved_skills), "user should have 3 skills")


def test_remove_user_skill(db_session):
    """Verifies that remove_user_skill removes a skill from a user."""
    log_info("[TEST] Ejecutando: test_remove_user_skill")
    
    # Create user and add skill
    user_data = UserCreate(
        email="removeskill@example.com",
        first_name="Remove",
        last_name="Skill",
        password="password123"
    )
    user = crud.create_user(db_session, user_data)
    
    skill_data = UserSkillCreate(skill_name="Kubernetes", points=8)
    crud.add_user_skill(db_session, user.id, skill_data)
    
    # Remove skill
    result = crud.remove_user_skill(db_session, user.id, "Kubernetes")
    
    log_assert_equal(True, result, "remove_user_skill returns True")
    
    # Verify skill is removed
    remaining_skills = crud.get_user_skills(db_session, user.id)
    log_assert_equal(0, len(remaining_skills), "user should have 0 skills")


def test_remove_nonexistent_skill(db_session):
    """Verifies that remove_user_skill returns False for non-existent skill."""
    log_info("[TEST] Ejecutando: test_remove_nonexistent_skill")
    
    # Create user
    user_data = UserCreate(
        email="nonskill@example.com",
        first_name="No",
        last_name="Skill",
        password="password123"
    )
    user = crud.create_user(db_session, user_data)
    
    result = crud.remove_user_skill(db_session, user.id, "NonExistent")
    
    log_assert_equal(False, result, "remove_user_skill returns False for non-existent skill")
