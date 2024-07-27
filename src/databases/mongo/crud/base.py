from typing import Any

from pymongo import ASCENDING
from pymongo import DESCENDING

from src.databases.exceptions import ObjectNotFoundError
from src.databases.mongo.collections import CollectionType
from src.databases.mongo.setup import AsyncIOMotorClientSession


class CRUD:
    collection: CollectionType

    @classmethod
    def _query(cls, query: dict) -> tuple[dict, list, int, int]:
        _filters, _sorting, _pagination = [query.get(key, None) for key in ["filters", "sorting", "pagination"]]

        filters = dict()
        for _filter in _filters:
            filters[_filter["field"]] = _filter["value"]

        sorting = []
        for _sort in _sorting:
            if _sort["type"] == "desc":
                sorting.append((_sort["field"], DESCENDING))
            else:
                sorting.append((_sort["field"], ASCENDING))

        if not sorting:
            sorting.append(("created_at", ASCENDING))

        limit, offset = _pagination.get("limit", 10), _pagination.get("offset", 0)

        return filters, sorting, limit, offset

    @classmethod
    async def get(cls, session: AsyncIOMotorClientSession, field: str, value: Any) -> CollectionType:
        document = await cls.collection.find_one({field: value}, session=session)
        if not document:
            raise ObjectNotFoundError
        return document

    @classmethod
    async def get_by_kwargs(cls, session: AsyncIOMotorClientSession, **kwargs) -> CollectionType:
        document = await cls.collection.find_one(kwargs, session=session)
        if not document:
            raise ObjectNotFoundError
        return document

    @classmethod
    async def get_list(cls, session: AsyncIOMotorClientSession, field: str, value: Any) -> list[CollectionType]:
        return await (cls.collection.find({field: value}, session=session)).to_list(length=None)

    @classmethod
    async def get_paginated(cls, session: AsyncIOMotorClientSession, query: dict) -> tuple[list[CollectionType], int]:
        filters, sorting, limit, offset = cls._query(query)
        documents = await (
            cls.collection.find(filters, session=session).sort(sorting).skip(offset).limit(limit).to_list(length=None)
        )
        total = await cls.collection.count_documents(filters, session=session)
        return documents, total

    @classmethod
    async def create(cls, session: AsyncIOMotorClientSession, model: dict) -> CollectionType:
        instance = await cls.collection.insert_one(model, session=session)
        return await cls.get(session, field="_id", value=instance.inserted_id)

    @classmethod
    async def update(cls, session: AsyncIOMotorClientSession, field: str, value: Any, **kwargs) -> None:
        await cls.collection.update_one({field: value}, {"$set": kwargs}, session=session)

    @classmethod
    async def delete(cls, session: AsyncIOMotorClientSession, field: str, value: Any) -> None:
        await cls.collection.delete_one({field: value}, session=session)
