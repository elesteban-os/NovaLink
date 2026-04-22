import os
import sys

# Agregamos el directorio actual al path para poder importar módulos de la app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app import models, security

def seed_users():
    # Asegurarnos de que las tablas existan
    print("Creando tablas en la base de datos (si no existen)...")
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    # Datos de prueba
    users_data = [
        {
            "first_name": "Juan",
            "last_name": "Pérez",
            "email": "juan.perez@example.com",
            "password": "password123",
            "skills": ["Python", "Docker", "Kubernetes"]
        },
        {
            "first_name": "Ana",
            "last_name": "García",
            "email": "ana.garcia@example.com",
            "password": "password123",
            "skills": ["JavaScript", "React", "Node.js"]
        },
        {
            "first_name": "Carlos",
            "last_name": "López",
            "email": "carlos.lopez@example.com",
            "password": "password123",
            "skills": ["Java", "Spring Boot", "SQL"]
        },
        {
            "first_name": "María",
            "last_name": "Rodríguez",
            "email": "maria.rodriguez@example.com",
            "password": "password123",
            "skills": ["Go", "Kubernetes", "AWS"]
        }
    ]

    try:
        for user_data in users_data:
            # Comprobar si el usuario ya existe
            existing_user = db.query(models.User).filter(models.User.email == user_data["email"]).first()
            if existing_user:
                print(f"El usuario {user_data['email']} ya existe. Omitiendo.")
                continue
            
            # Hashear la contraseña
            hashed_pw = security.get_password_hash(user_data["password"])
            
            # Crear modelo de usuario
            new_user = models.User(
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                hashed_password=hashed_pw
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            print(f"Usuario creado: {new_user.first_name} {new_user.last_name}")
            
            # Añadir sus skills
            for skill in user_data["skills"]:
                new_skill = models.UserSkill(
                    user_id=new_user.id,
                    skill_name=skill
                )
                db.add(new_skill)
            
            db.commit()
            print(f"  -> Skills añadidas para {new_user.first_name}: {', '.join(user_data['skills'])}")

        print("\n¡Población de usuarios y habilidades completada con éxito!")
        
    except Exception as e:
        print(f"Error al poblar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()