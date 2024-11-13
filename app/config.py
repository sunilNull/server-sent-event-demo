from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Task Status Service"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./tasks.db"
    REDIS_URL: Optional[str] = None  # Optional Redis for scaling
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
