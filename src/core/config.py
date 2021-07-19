from src.db.settings import SQLiteDBSettings

configs = [SQLiteDBSettings]


class Settings(*configs):
    API_URL: str = "/api/v1"


settings = Settings()
