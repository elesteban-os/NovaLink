"""Logger configuration for the notifications service."""

import logging

logger = logging.getLogger("notifications_service")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("[%(asctime)s] [%(levelname)s] [notifications] %(message)s")
)
logger.addHandler(handler)
