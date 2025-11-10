# src/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
import pytz

class Settings(BaseSettings):
    # Environment
    TIMEZONE: str = "Asia/Dhaka"
    DEBUG: bool = True
    APP_ENV: str = "dev"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8080
    
    # App
    APP_NAME: str = "deed"
    STATIC_VERSION: str = "1.0.83"
    SITE_BASE_URL: str = "http://127.0.0.1:8080"
    
    # Security/CSRF settings
    SECRET_KEY: str = "Wnj78@kjdfnG7$kdtfgrt456#kdfjG7!kdfjG7!"
    COOKIE_SAMESITE: str = "Lax"
    COOKIE_SECURE: bool = False  # Set to False for local dev (HTTPS required for True)
    COOKIE_DOMAIN: Optional[str] = None
    HEADER_NAME: str = "X-CSRF-Token"
    COOKIE_NAME: str = "csrf_access_token"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://deedadmin:deedadmin@127.0.0.1:5432/deed"
    
    # Company
    COMPANY_NAME: str = "deed"
    COMPANY_PHONE: str = "+880-1XXXXXXXXX"
    COMPANY_EMAIL: str = "info@deed.com"
    COMPANY_ADDRESS: str = "Panthapath, Dhaka, Bangladesh"
    
    # Computed properties
    @property
    def timezone(self):
        return pytz.timezone(self.TIMEZONE)
    
    @property
    def is_development(self):
        return self.APP_ENV == "dev"
    
    @property
    def template_dir(self):
        return "src/backend/templates"
    
    @property
    def static_dir(self):
        return "src/backend/static"

    class Config:
        env_file = ".env"
        extra = "ignore"  # This line tells Pydantic to ignore extra fields not defined in the model

@lru_cache()
def get_settings() -> Settings:
    return Settings()