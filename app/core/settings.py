from typing import Optional

from pydantic import ValidationInfo
from pydantic import field_validator
from pydantic_settings import BaseSettings


class PostgresDBSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_ECHO: bool = False

    POSTGRES_URI: Optional[str] = None

    @field_validator("POSTGRES_URI")
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> str:
        if isinstance(v, str):
            return v
        # Return URL-connect 'postgresql://postgres:password@localhost:5432/invoices'
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
            user=values.data["POSTGRES_USER"],
            password=values.data["POSTGRES_PASSWORD"],
            host=values.data["POSTGRES_HOST"],
            port=values.data["POSTGRES_PORT"],
            db=values.data["POSTGRES_DB"],
        )


class LoggerSetting(BaseSettings):
    LOGGER_CONSOLE: bool
    LOGGER_CONSOLE_LEVEL: str

    LOGGER_GRAYLOG: bool
    LOGGER_GRAYLOG_LEVEL: str
    LOGGER_GRAYLOG_HOST: str
    LOGGER_GRAYLOG_PORT: int


class TracingSettings(BaseSettings):
    TRACING: bool
    TRACING_LEVEL: str
    TRACING_ENDPOINT: str


class KafkaSetting(BaseSettings):
    KAFKA: bool
    KAFKA_BOOTSTRAP_SERVER: str


class SentrySettings(BaseSettings):
    SENTRY: bool
    SENTRY_DSN: Optional[str]
    SENTRY_ENVIRONMENT: str


settings = [
    PostgresDBSettings,
    LoggerSetting,
    TracingSettings,
    KafkaSetting,
    SentrySettings,
]


class AppSettings(*settings):
    PROJECT_NAME: str
    ENV: str
    API_PREFIX: str
    API_DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True


config = AppSettings()
