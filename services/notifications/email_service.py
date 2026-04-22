"""
Servicio de Email - Simulación de envío de notificaciones
Imprime mensajes de email en consola/logs para propósitos de desarrollo.
"""

import logging
from datetime import datetime
from models import Notification

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


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
    
    # Registrar en logs del servidor
    logger.info(f"Enviando notificacion por email - Notification ID: {notification.id}, User ID: {notification.user_id}")
    logger.info(f"Asunto: {notification.title}")
    logger.info(f"Descripcion: {notification.description}")
    
    # Imprimir en consola para visibilidad inmediata
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

