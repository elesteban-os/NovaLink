import os


class Settings:
    """Configuración de entorno para el servicio Auth."""

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "auth_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres_auth")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    DB_ECHO: bool = os.getenv("DB_ECHO", "False").lower() in ("1", "true", "yes")

    API_TITLE: str = os.getenv("API_TITLE", "Auth Microservice")
    API_DESCRIPTION: str = os.getenv("API_DESCRIPTION", "Servicio de autenticación NovaLink")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8007"))

    JWT_SECRET: str = os.getenv("JWT_SECRET", "SUPER_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
