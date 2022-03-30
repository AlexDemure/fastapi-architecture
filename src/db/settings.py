from pydantic import BaseSettings


class SQLiteDBSettings(BaseSettings):

    SQLITE_URI = "sqlite://db.sqlite3"
