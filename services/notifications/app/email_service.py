"""
Servicio de Email - Simulación de envío de notificaciones
Imprime mensajes de email en consola/logs para propósitos de desarrollo.
"""

from datetime import datetime

from .logger import logger
from .models import Notification


def send_email(notification: Notification) -> dict:
    """
    Simula envío de notificación imprimiendo en consola/logs.
    Retorna diccionario con detalles del envío simulado.
    """
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Crear mensaje de email formateado
    email_body = f"""
╔════════════════════════════════════════════════════════════╗
║                    NOTIFICACION DE CORREO                  ║
╚════════════════════════════════════════════════════════════╝

FECHA DE ENVIO: {timestamp}
NOTIFICATION ID: {notification.id}
USER ID: {notification.user_id}
ORDER ID: {notification.order_id}

ASUNTO: {notification.title}

CONTENIDO:
{'-' * 56}
{notification.description}
{'-' * 56}

ESTADO: ENVIADO (SIMULADO)

════════════════════════════════════════════════════════════
Este es un envio simulado para fines de desarrollo.
En produccion se utilizaria un servicio de email real.
════════════════════════════════════════════════════════════
"""
    
    # Log the simulated email send event
    logger.info(f"Sending notification email - Notification ID: {notification.id}, User ID: {notification.user_id}")
    logger.info(f"Subject: {notification.title}")
    logger.info(f"Description: {notification.description}")
    
    # Print email body to console for development visibility
    print(email_body)
    
    return {
        "status": "sent",
        "notification_id": notification.id,
        "user_id": notification.user_id,
        "order_id": notification.order_id,
        "title": notification.title,
        "timestamp": timestamp,
        "simulated": True
    }

