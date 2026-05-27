import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Environment settings for the Users service."""
    
    # ===== DATABASE =====
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field("postgres_users", env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_ECHO: bool = Field(False, env="DB_ECHO")
    
    # ===== API =====
    API_TITLE: str = Field("Users Microservice", env="API_TITLE")
    API_DESCRIPTION: str = Field("Microservicio de gestión de usuarios", env="API_DESCRIPTION")
    API_VERSION: str = Field("1.0.0", env="API_VERSION")
    
    # ===== SERVER =====
    SERVER_HOST: str = Field("0.0.0.0", env="SERVER_HOST")
    SERVER_PORT: int = Field(8001, env="SERVER_PORT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct the database connection URL from environment variables or override."""
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            return env_url
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


# Instancia global
settings = Settings()
