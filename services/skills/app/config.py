from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Environment configuration for the skills service."""
    
    # ===== DATABASE =====
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_ECHO: bool = False
    
    # ===== API =====
    API_TITLE: str = "Skills Microservice"
    API_DESCRIPTION: str = "Microservicio de gestión de habilidades"
    API_VERSION: str = "1.0.0"
    
    # ===== SERVER =====
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    
    @property
    def DATABASE_URL(self) -> str:
        """Build the database URL."""
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


# Global instance
settings = Settings()
