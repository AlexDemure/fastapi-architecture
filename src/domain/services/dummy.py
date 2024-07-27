from src.databases.mongo import mongoconnect
from src.databases.postgres import pgconnect
from src.domain import models
from src.domain import repositories


class Dummy:
    @classmethod
    async def get(cls, dummy_id: int) -> models.Dummy:
        async with pgconnect() as session:
            return await repositories.Dummy.get(session, model_id=dummy_id)

    @classmethod
    async def create(cls) -> models.Dummy:
        async with pgconnect(transaction=True) as session:
            return await repositories.Dummy.create(session, model=models.Dummy.init())


class DummyDocument:
    @classmethod
    async def get(cls, dummy_id: str) -> models.Dummy:
        async with mongoconnect() as session:
            return await repositories.DummyDocument.get(session, model_id=dummy_id)

    @classmethod
    async def create(cls) -> models.Dummy:
        async with mongoconnect(transaction=True) as session:
            return await repositories.DummyDocument.create(session, model=models.DummyDocument.init())
