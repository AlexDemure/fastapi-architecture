from enum import Enum
from typing import Any
from typing import Optional

from pydantic import FieldValidationInfo
from pydantic import PostgresDsn
from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Env(str, Enum):
    develop = "develop"
    production = "production"


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgresql+asyncpg"}


class PostgresSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    POSTGRES_URI: Optional[AsyncPostgresDsn] = None

    @field_validator("POSTGRES_URI", mode="after")
    def assemble_postgres_connection(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        # Return URL-connect 'postgresql://postgres:password@localhost:5432/store'
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data["POSTGRES_USER"],
            password=info.data["POSTGRES_PASSWORD"],
            host=info.data["POSTGRES_HOST"],
            port=info.data["POSTGRES_PORT"],
            path=info.data["POSTGRES_DB"],
        )


class MongoSettings(BaseSettings):
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_DB: str

    MONGO_URI: Optional[str] = None

    @field_validator("MONGO_URI", mode="after")
    def assemble_mongo_connection(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        # Return URL-connect 'mongodb://mongo:mongo@localhost:27017'
        return "mongodb://{user}:{password}@{host}:{port}/{db}".format(
            user=info.data["MONGO_USER"],
            password=info.data["MONGO_PASSWORD"],
            host=info.data["MONGO_HOST"],
            port=info.data["MONGO_PORT"],
            db=info.data["MONGO_DB"],
        )


class LoggerSetting(BaseSettings):
    LOGGER_CONSOLE: bool
    LOGGER_CONSOLE_LEVEL: str


class S3Settings(BaseSettings):
    S3_URL: str
    S3_ACCESS_KEY_ID: str
    S3_SECRET_KEY: str
    S3_BUCKET: str


class JWTSettings(BaseSettings):
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_ACCESS_EXPIRED_SECONDS: int
    JWT_REFRESH_EXPIRED_SECONDS: int


# INCLUDE SETTINGS
configs = [
    PostgresSettings,
    MongoSettings,
    LoggerSetting,
    S3Settings,
    JWTSettings,
]


class Settings(*configs):  # type:ignore
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    SERVER_HOST: str
    SERVER_PORT: int
    SERVER_ENV: Env
    SERVER_NAME: str
    SERVER_API_PATH: str


settings = Settings()
