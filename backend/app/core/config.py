"""
Central application configuration.
All values are read from environment variables (see backend/.env.example).
Nothing sensitive is hard-coded.
"""
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    DATABASE_URL: str = "postgresql+psycopg2://civicai:civicai@localhost:5432/civicai"
    USE_SQLITE: bool = True
    SQLITE_PATH: str = "./civicai.db"

    # Auth
    JWT_SECRET: str = "change_this_super_secret_key_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # AI
    AI_MODE: str = "demo"  # demo | live
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Storage
    STORAGE_PROVIDER: str = "local"  # local | supabase
    LOCAL_UPLOAD_DIR: str = "../uploads"
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    SUPABASE_BUCKET: str = "civicai-uploads"

    # Deadlines (hours) - configurable defaults, overridden at runtime by SystemSetting table
    ACKNOWLEDGEMENT_DEADLINE_HOURS: float = 6
    CRITICAL_RESOLUTION_HOURS: float = 12
    HIGH_RESOLUTION_HOURS: float = 24
    MEDIUM_RESOLUTION_HOURS: float = 48
    LOW_RESOLUTION_HOURS: float = 72

    # Duplicate detection
    TEXT_SIMILARITY_THRESHOLD: float = 0.70
    DUPLICATE_RADIUS_METERS: float = 100

    # Scheduler
    SCHEDULER_INTERVAL_MINUTES: float = 1

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> "Settings":
    return Settings()
