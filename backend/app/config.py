from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = Field(default=8000, ge=1, le=65535)
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "taskflow"
    jwt_secret_key: str = Field(min_length=32)
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = Field(default=30, gt=0)
    auth_cookie_name: str = "taskflow_auth"
    csrf_cookie_name: str = "taskflow_csrf"
    cookie_secure: bool = False
    cookie_samesite: str = "lax"
    allowed_origins: str = "http://localhost:8000"
    log_level: str = "INFO"

    @property
    def allowed_origin_values(self) -> set[str]:
        return {
            origin.strip().rstrip("/")
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
