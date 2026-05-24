import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings_for_postqresql(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE",Path(__file__).resolve().parent.parent/".env")
    )


settings = Settings_for_postqresql()


def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")