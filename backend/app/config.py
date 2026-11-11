from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    database_url: str
    db_echo: bool = False
    jwt_secret: str                      
    jwt_algorithm: str = "HS256"
    access_ttl_minutes: int = 15
    refresh_ttl_hours: int = 24
    cookie_secure: bool = False          
    admin_email: str | None = None 
    admin_password: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()