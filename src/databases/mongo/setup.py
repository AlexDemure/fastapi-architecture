from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorClientSession

from src.framework import settings

client = AsyncIOMotorClient(settings.MONGO_URI)

mongodb = client[settings.MONGO_DB]


@asynccontextmanager
async def mongoconnect(transaction: bool = False) -> AsyncIOMotorClientSession:
    async with await client.start_session() as session:
        if transaction:
            async with session.start_transaction() as _:
                yield session
        else:
            yield session
