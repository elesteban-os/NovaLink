import logging
import sys
from typing import Optional


class LoggerSetup:
    """Configuración centralizada de logging."""
    
    _logger: Optional[logging.Logger] = None
    
    @classmethod
    def get_logger(cls, name: str = __name__) -> logging.Logger:
        """
        Obtener logger configurado.
        
        Args:
            name: Nombre del módulo (normalmente __name__)
            
        Returns:
            Instancia de logger configurada
        """
        if cls._logger is None:
            # Configurar formato
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            
            # Handler a stdout
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            
            # Crear logger
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            logger.addHandler(handler)
            
            cls._logger = logger
        
        return cls._logger


# Instancia global
logger = LoggerSetup.get_logger(__name__)
