from src.databases import Session
from src.databases import mongo
from src.databases import postgres
from src.domain import models

from .base import Repository


class Dummy(Repository):
    db = postgres.Dummy
    model = models.Dummy

    @classmethod
    async def get(cls, session: Session, model_id: int) -> "Dummy.model":
        row = await cls.db.get(session, field=cls.pk(), value=cls.id(model_id))
        return cls.model.orm(row)


class DummyDocument(Repository):
    db = mongo.Dummy
    model = models.DummyDocument

    @classmethod
    async def get(cls, session: Session, model_id: str) -> "DummyDocument.model":
        document = await cls.db.get(session, field=cls.pk(), value=cls.id(model_id))
        return cls.model.orm(document)
