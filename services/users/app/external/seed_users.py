from app.database import Base, SessionLocal, engine
from app.logger import logger
from app.persistence import crud
from app.persistence.schemas import UserCreate, UserSkillCreate


def seed_users() -> None:
    Base.metadata.create_all(bind=engine)

    users_data = [
        {
            "first_name": "Juan",
            "last_name": "Pérez",
            "email": "juan.perez@admin.com",
            "password": "password123",
            "skills": ["empatía", "liderazgo", "comunicación"]
        },
        {
            "first_name": "Ana",
            "last_name": "García",
            "email": "ana.garcia@admin.com",
            "password": "password123",
            "skills": ["creatividad", "colaboración", "adaptabilidad"]
        },
        {
            "first_name": "Carlos",
            "last_name": "López",
            "email": "carlos.lopez@user.com",
            "password": "password123",
            "skills": ["resiliencia", "paciencia", "confianza"]
        },
        {
            "first_name": "María",
            "last_name": "Rodríguez",
            "email": "maria.rodriguez@user.com",
            "password": "password123",
            "skills": ["escucha activa", "iniciativa", "sagacidad"]
        }
    ]

    db = SessionLocal()
    try:
        for user_data in users_data:
            if crud.get_user_by_email(db, user_data["email"]):
                logger.info(f"El usuario {user_data['email']} ya existe. Omitiendo semilla.")
                continue

            user_create = UserCreate(
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                password=user_data["password"],
            )
            user = crud.create_user(db, user_create)

            for skill_name in user_data["skills"]:
                skill_create = UserSkillCreate(skill_name=skill_name)
                crud.add_user_skill(db, user.id, skill_create)

            logger.info(f"Usuario semillado: {user.email}")
    except Exception as exc:
        logger.error(f"Error al poblar usuarios: {exc}")
        db.rollback()
        raise
    finally:
        db.close()
