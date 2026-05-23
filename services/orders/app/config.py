from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from .env and environment variables."""

    DB_USER: str = Field(...)
    DB_PASSWORD: str = Field(...)
    DB_HOST: str = Field(...)
    DB_PORT: int = Field(5432)
    DB_NAME: str = Field(...)
    DB_ECHO: bool = Field(False)

    JWT_SECRET: str = Field("SUPER_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256")

    SERVER_HOST: str = Field("0.0.0.0")
    SERVER_PORT: int = Field(8005)

    @property
    def SECRET_KEY(self) -> str:
        return self.JWT_SECRET

    @property
    def ALGORITHM(self) -> str:
        return self.JWT_ALGORITHM

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
