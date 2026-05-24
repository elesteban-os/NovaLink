import logging
import sys


class LoggerSetup:
    """Centralized logging setup for the Auth service."""

    @staticmethod
    def get_logger(name: str = __name__) -> logging.Logger:
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger


logger = LoggerSetup.get_logger("auth")
