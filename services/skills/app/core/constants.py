from enum import Enum


class SkillDifficulty(int, Enum):
    """Niveles de dificultad de skills."""
    TRIVIAL = 0
    VERY_EASY = 1
    EASY = 2
    MEDIUM_EASY = 3
    MEDIUM = 4
    MEDIUM_HARD = 5
    HARD = 6
    VERY_HARD = 7
    EXTREME = 8
    MASTER = 9
    LEGENDARY = 10


# Constantes de negocio
MIN_DIFFICULTY = 0
MAX_DIFFICULTY = 10
DEFAULT_STOCK = 0
