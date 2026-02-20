"""Application configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings loaded from environment."""

    environment: str = "development"
    debug: bool = True
    secret_key: str = "dev-secret-key"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/cultivar-saasdev"
    redis_url: str = "redis://localhost:6379/0"
    allowed_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


settings = Settings()
