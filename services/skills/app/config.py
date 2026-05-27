from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Environment configuration for the skills service."""
    
    # ===== DATABASE =====
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_ECHO: bool = Field(False, env="DB_ECHO")

    # ===== RABBITMQ =====
    RABBITMQ_HOST: str = Field("novalink-rabbitmq", env="RABBITMQ_HOST")
    RABBITMQ_PORT: int = Field(5672, env="RABBITMQ_PORT")
    RABBITMQ_USER: str = Field("guest", env="RABBITMQ_USER")
    RABBITMQ_PASSWORD: str = Field("guest", env="RABBITMQ_PASSWORD")
    RABBITMQ_VHOST: str = Field("/", env="RABBITMQ_VHOST")
    
    # ===== API =====
    API_TITLE: str = Field("Skills Microservice", env="API_TITLE")
    API_DESCRIPTION: str = Field("Microservicio de gestión de habilidades", env="API_DESCRIPTION")
    API_VERSION: str = Field("1.0.0", env="API_VERSION")
    
    # ===== SERVER =====
    SERVER_HOST: str = Field("0.0.0.0", env="SERVER_HOST")
    SERVER_PORT: int = Field(8000, env="SERVER_PORT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
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
