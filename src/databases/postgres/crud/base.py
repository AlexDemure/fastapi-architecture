from typing import Any

from sqlalchemy import delete
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import Select

from src.databases.exceptions import ObjectNotFoundError
from src.databases.postgres.setup import AsyncSession
from src.databases.postgres.tables import TableType


class CRUD:
    table: TableType

    @classmethod
    def _query(cls, query: dict) -> tuple[list, list, int, int]:
        _filters, _sorting, _pagination = [query.get(key, None) for key in ["filters", "sorting", "pagination"]]

        filters = []
        for _filter in _filters:
            filters.append(getattr(cls.table, _filter["field"]) == _filter["value"])

        sorting = []
        for _sort in _sorting:
            if _sort["type"] == "desc":
                sorting.append(desc(getattr(cls.table, _sort["field"])))
            else:
                sorting.append(getattr(cls.table, _sort["field"]))

        limit, offset = _pagination.get("limit", 10), _pagination.get("offset", 0)

        return filters, sorting, limit, offset

    @classmethod
    async def get(cls, session: AsyncSession, field: str, value: Any) -> TableType:
        query = select(cls.table).where(getattr(cls.table, field) == value)
        return await get_one(session, query)

    @classmethod
    async def get_by_kwargs(cls, session: AsyncSession, **kwargs) -> TableType:
        filters = []

        for key in kwargs.keys():
            if isinstance(kwargs[key], list):
                filters.append(getattr(cls.table, key).in_(kwargs[key]))
            else:
                filters.append(getattr(cls.table, key) == kwargs[key])

        query = select(cls.table).where(*filters)

        return await get_one(session, query)

    @classmethod
    async def get_list(cls, session: AsyncSession, field: str, value: Any) -> list[TableType]:
        filters = []

        if isinstance(value, list):
            filters.append(getattr(cls.table, field).in_(value))
        else:
            filters.append(getattr(cls.table, field) == value)

        query = select(cls.table).where(*filters)

        return await get_list(session, query)

    @classmethod
    async def get_paginated(cls, session: AsyncSession, query: dict) -> tuple[list[TableType], int]:
        filters, sorting, limit, offset = cls._query(query)
        query = select(cls.table).where(*filters).order_by(*sorting)
        total = await get_count(session, query)
        rows = await get_list(session, query.limit(limit).offset(offset))
        return rows, total

    @classmethod
    async def create(cls, session: AsyncSession, model: dict) -> TableType:
        created_fields = {k: v for k, v in model.items() if getattr(cls.table, k, None) is not None}
        instance = cls.table(**created_fields)
        session.add(instance)
        await session.flush()
        return instance

    @classmethod
    async def update(cls, session: AsyncSession, field: str, value: Any, **kwargs) -> None:
        updated_fields = {k: v for k, v in kwargs.items() if getattr(cls.table, k, None) is not None}
        query = update(cls.table).where(getattr(cls.table, field) == value).values(**updated_fields)
        await session.execute(query)
        await session.flush()

    @classmethod
    async def delete(cls, session: AsyncSession, field: str, value: Any) -> None:
        query = delete(cls.table).where(getattr(cls.table, field) == value)
        await session.execute(query)
        await session.flush()


async def get_list(session: AsyncSession, query: Select) -> list[TableType]:
    return (await session.execute(query)).scalars().all()  # type:ignore


async def get_one(session: AsyncSession, query: Select) -> TableType:
    try:
        return (await session.execute(query)).unique().scalars().one()
    except NoResultFound:
        raise ObjectNotFoundError


async def get_count(session: AsyncSession, query: Select) -> int:
    return (await session.execute(select(func.count()).select_from(query.subquery()))).scalars().one()
