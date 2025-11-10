# src/backend/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "deed"
    DEBUG: bool = True
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    #DATABASE_URL: str = "postgresql+asyncpg://deedadmin:deedadmin@127.0.0.1:5432/deeddb"
    #DATABASE_URL: str = "postgresql+asyncpg://neondb_owner:npg_SO24LIGJZNkh@ep-lucky-fire-a112h5hp-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    DATABASE_URL: str = "postgresql+asyncpg://neondb_owner:npg_orxp76UyDTJC@ep-orange-resonance-a1xuwcup-pooler.ap-southeast-1.aws.neon.tech/deed_db"
    SECRET_KEY: str = "change-me"

    # NEW: read version from .env (e.g., STATIC_VERSION=1.0.0)
    STATIC_VERSION: str = "dev-001"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
