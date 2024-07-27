from datetime import datetime
from typing import Union

from bson import ObjectId

from src.databases import Session
from src.databases import mongo
from src.databases import postgres
from src.domain.models import Model


class Repository:
    db: Union[postgres.ORM, mongo.ORM]
    model: Model

    @classmethod
    def id(cls, model_id: Union[str, int]) -> Union[str, int, ObjectId]:
        if issubclass(cls.db, postgres.ORM):
            return model_id
        elif issubclass(cls.db, mongo.ORM):
            return ObjectId(model_id)
        else:
            raise NotImplementedError

    @classmethod
    def pk(cls) -> str:
        if issubclass(cls.db, postgres.ORM):
            return "id"
        elif issubclass(cls.db, mongo.ORM):
            return "_id"
        else:
            raise NotImplementedError

    @classmethod
    async def get_list_by_ids(cls, session: Session, model_ids: list[Union[str, int]]) -> list["Repository.model"]:
        rows = await cls.db.get_list(session, field=cls.pk(), value=[cls.id(model_id) for model_id in model_ids])
        return [cls.model.orm(row) for row in rows]

    @classmethod
    async def get_paginated(cls, session: Session, query: dict) -> tuple[list["Repository.model"], int]:
        rows, total = await cls.db.get_paginated(session, query=query)
        return [cls.model.orm(row) for row in rows], total

    @classmethod
    async def create(cls, session: Session, model: dict) -> "Repository.model":
        row = await cls.db.create(session, model)
        return cls.model.orm(row)

    @classmethod
    async def update(cls, session: Session, model_id: Union[str, int], **kwargs) -> None:
        await cls.db.update(
            session=session,
            field=cls.pk(),
            value=cls.id(model_id),
            updated_at=datetime.utcnow(),
            **kwargs,
        )

    @classmethod
    async def delete(cls, session: Session, model_id: Union[str, int]) -> None:
        return await cls.db.delete(session, field=cls.pk(), value=cls.id(model_id))
