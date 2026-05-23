from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from .env and environment variables."""

    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_ECHO: bool = Field(False, env="DB_ECHO")

    EMAIL_HOST: str = Field("localhost", env="EMAIL_HOST")
    EMAIL_PORT: int = Field(25, env="EMAIL_PORT")
    EMAIL_USER: str | None = Field(None, env="EMAIL_USER")
    EMAIL_PASSWORD: str | None = Field(None, env="EMAIL_PASSWORD")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
