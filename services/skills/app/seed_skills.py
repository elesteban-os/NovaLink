from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

load_dotenv(BASE_DIR / ".env")

from app.db import SessionLocal, engine  # noqa: E402
from app import models  # noqa: E402

SKILLS = [
    {"skill_name": "empatía", "difficulty_level": 3, "stock": 280},
    {"skill_name": "amistad", "difficulty_level": 2, "stock": 300},
    {"skill_name": "liderazgo", "difficulty_level": 9, "stock": 45},
    {"skill_name": "creatividad", "difficulty_level": 7, "stock": 95},
    {"skill_name": "resiliencia", "difficulty_level": 8, "stock": 70},
    {"skill_name": "comunicación", "difficulty_level": 5, "stock": 160},
    {"skill_name": "colaboración", "difficulty_level": 4, "stock": 190},
    {"skill_name": "sagacidad", "difficulty_level": 9, "stock": 40},
    {"skill_name": "paciencia", "difficulty_level": 3, "stock": 250},
    {"skill_name": "respeto", "difficulty_level": 2, "stock": 300},
    {"skill_name": "confianza", "difficulty_level": 4, "stock": 180},
    {"skill_name": "humor", "difficulty_level": 2, "stock": 220},
    {"skill_name": "adaptabilidad", "difficulty_level": 6, "stock": 120},
    {"skill_name": "escucha activa", "difficulty_level": 5, "stock": 140},
    {"skill_name": "iniciativa", "difficulty_level": 8, "stock": 60},
]


def seed_skills() -> None:
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        for skill_data in SKILLS:
            db.add(
                models.Skill(
                    skill_name=skill_data["skill_name"],
                    difficulty_level=skill_data["difficulty_level"],
                    stock=skill_data["stock"],
                )
            )

        db.commit()


if __name__ == "__main__":
    seed_skills()
    print("Base de datos de skills poblada correctamente.")
