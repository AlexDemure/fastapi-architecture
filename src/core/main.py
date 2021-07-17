import uvicorn

from fastapi import FastAPI

from src.db.database import sqlite_db_init

app = FastAPI()


@app.on_event("startup")
async def connect_db():
    print("Connection to SQLite3...")
    await sqlite_db_init()


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=7040, log_level="debug")
