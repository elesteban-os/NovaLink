"""Logging configuration for the skills service."""

import logging
import sys
from typing import Optional


class LoggerSetup:
    """Centralized logging configuration."""
    
    _logger: Optional[logging.Logger] = None
    
    @classmethod
    def get_logger(cls, name: str = __name__) -> logging.Logger:
        """
        Get a configured logger.
        
        Args:
            name: Module name (normally __name__)
            
        Returns:
            Configured logger instance
        """
        if cls._logger is None:
            # Configure formatting
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            
            # Handler to stdout
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            
            # Create logger
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            logger.addHandler(handler)
            
            cls._logger = logger
        
        return cls._logger


# Global instance
logger = LoggerSetup.get_logger(__name__)
