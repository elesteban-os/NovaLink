from enum import Enum


class UserRole(str, Enum):
    """Roles válidos para usuarios."""

    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


MAX_USER_SKILL_POINTS = 100
MIN_USER_SKILL_POINTS = 1
