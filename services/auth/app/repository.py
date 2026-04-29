from sqlalchemy.orm import Session
from . import models

class AuthRepository:
    def get_user_by_email(self, db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()