import logging
from typing import Optional


class LoggerSetup:
    """Configuración centralizada de logging."""
    
    _logger: Optional[logging.Logger] = None
    
    @classmethod
    def get_logger(cls, name: str = __name__) -> logging.Logger:
        """
        Obtener logger configurado.
        
        Args:
            name: Nombre del logger (usualmente __name__)
            
        Returns:
            Logger configurado
        """
        if cls._logger is None:
            cls._logger = logging.getLogger(name)
            
            # Solo configurar si no tiene handlers
            if not cls._logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                handler.setFormatter(formatter)
                cls._logger.addHandler(handler)
                cls._logger.setLevel(logging.INFO)
        
        return cls._logger


# Instancia global
logger = LoggerSetup.get_logger(__name__)
