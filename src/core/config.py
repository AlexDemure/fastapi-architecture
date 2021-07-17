from db.settings import SQLiteDBSettings

configs = [SQLiteDBSettings,]


class Settings(*configs):
    pass


settings = Settings()
