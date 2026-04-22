"""
Modelos SQLAlchemy para la tabla de notificaciones.
Define la estructura de la base de datos.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base
from datetime import datetime


class Notification(Base):
    """
    Modelo de notificación en la base de datos.
    
    Atributos:
        id: Identificador único de la notificación
        user_id: ID del usuario que recibe la notificación
        order_id: ID del pedido asociado a la notificación
        title: Título de la notificación
        description: Descripción detallada de la notificación
        created_at: Fecha y hora de creación (generada automáticamente)
    """
    
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    order_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        """Representación en string del objeto."""
        return f"<Notification(id={self.id}, user_id={self.user_id}, order_id={self.order_id})>"
