import logging

logger = logging.getLogger("orders_service")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("[%(asctime)s] [%(levelname)s] [orders] %(message)s")
)
logger.addHandler(handler)
