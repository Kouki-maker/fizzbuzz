from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Configuration de l'application"""

    # Application
    PROJECT_NAME: str = "API Statistics Tracker"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "dev"
    DEBUG: bool = False


    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "db"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text

    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]

    # Stats
    STATS_BATCH_SIZE: int = 100
    STATS_FLUSH_INTERVAL: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Retourne l'instance singleton des settings"""
    return Settings()


settings = get_settings()
