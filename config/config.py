import base64
from functools import cached_property

from pydantic import HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class AppSettings(EnvSettings):
    SECRET_KEY: str
    DEBUG: bool = False
    ALLOWED_HOSTS: list[str] = ["*"]
    LOG_LEVEL: str = "DEBUG"
    PASSWORD_RESET_TIMEOUT: int = 60 * 60 * 4
    ADMIN_PANEL_URL: str = "admin/"
    DJANGO_SUPERUSER_EMAIL: str
    DJANGO_SUPERUSER_USERNAME: str
    DJANGO_SUPERUSER_PASSWORD: str
    DADATA_API_KEY: str
    DADATA_SECRET_KEY: str
    JWT_SECRET_KEY: str

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def log_set_correctly(cls, val: str) -> str:
        if val.lower() not in ("debug", "info", "warning", "error"):
            raise ValueError(
                f"LOG_LEVEL must be specified correctly. Got: {val}"
            )
        return val


class CORSSettings(EnvSettings):
    CSRF_TRUSTED_ORIGINS: list[str] = ["http://127.0.0.1"]
    CORS_ORIGIN_WHITELIST: list[str] = ["http://127.0.0.1"]
    CORS_ALLOW_ALL_ORIGINS: bool = True
    CORS_ALLOW_CREDENTIALS: bool = True


class DatabaseSettings(EnvSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int


class GunicornSettings(EnvSettings):
    GUNICORN_WORKERS: int = 2
    GUNICORN_THREADS: int = 2
    GUNICORN_LOGLEVEL: str = "debug"
    GUNICORN_BACKLOG: int = 2048
    GUNICORN_WORKER_CONNECTIONS: int = 1000
    GUNICORN_MAX_REQUESTS: int = 3500
    GUNICORN_MAX_REQUESTS_JITTER: int = 300
    GUNICORN_GRACEFUL_TIMEOUT: int = 15
    GUNICORN_KEEPALIVE: int = 5



class Config(EnvSettings):
    app: AppSettings = AppSettings()
    cors: CORSSettings = CORSSettings()
    database: DatabaseSettings = DatabaseSettings()
    gunicorn: GunicornSettings = GunicornSettings()


config = Config()
