import logging
from typing import Optional


class LoggerSetup:
    """Centralized logging configuration for the Users service."""

    _logger: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls, name: str = __name__) -> logging.Logger:
        """Return a configured logger instance for the given name."""
        if cls._logger is None:
            cls._logger = logging.getLogger(name)

            # Configure only when no handlers are present
            if not cls._logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
                handler.setFormatter(formatter)
                cls._logger.addHandler(handler)
                cls._logger.setLevel(logging.INFO)

        return cls._logger


# Global logger instance
logger = LoggerSetup.get_logger(__name__)
