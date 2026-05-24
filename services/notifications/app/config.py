"""Application configuration settings for the notifications service."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment and database configuration for notifications."""

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_ECHO: bool = False

    EMAIL_HOST: str = "localhost"
    EMAIL_PORT: int = 25
    EMAIL_USER: str | None = None
    EMAIL_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def DATABASE_URL(self) -> str:
        """Build the PostgreSQL database URL from environment settings."""
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
