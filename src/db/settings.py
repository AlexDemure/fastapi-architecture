from pydantic import BaseSettings, PostgresDsn, validator


class SQLiteDBSettings(BaseSettings):

    SQLITE_URI = "sqlite://db.sqlite3"
