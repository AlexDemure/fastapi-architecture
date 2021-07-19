import uvicorn
from fastapi import FastAPI

from src.core import middleware
from src.core.config import settings
from src.core.urls import api_router
from src.db.database import sqlite_db_init

app = FastAPI(
    middleware=middleware.utils
)


@app.on_event("startup")
async def connect_db():
    print("Connection to SQLite3...")
    await sqlite_db_init()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(api_router, prefix=settings.API_URL)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=7040, log_level="debug")
