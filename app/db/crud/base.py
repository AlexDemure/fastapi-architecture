from typing import Any
from typing import List
from typing import Type
from typing import TypeVar

from sqlalchemy import delete
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from app.db.setup import Base
from app.exceptions.crud import ObjectNotFoundError

Table = TypeVar("Table", bound=Base)


class CRUDBase:
    table: Type[Table]

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> Table:
        created_fields = {k: v for k, v in kwargs.items() if getattr(cls.table, k, None) is not None}
        instance = cls.table(**created_fields)
        session.add(instance)
        await session.flush()
        return instance

    @classmethod
    async def get(cls, session: AsyncSession, field: str, value: Any) -> Table:
        query = select(cls.table).where(getattr(cls.table, field) == value)
        return await exactly_one(session, query)

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


async def get_list(session: AsyncSession, query: Select) -> List[Table]:
    return (await session.execute(query)).scalars().all()


async def exactly_one(session: AsyncSession, query) -> Table:
    """sqlalchemy.exc.NoResultFound, sqlalchemy.exc.MultipleResultFound"""
    try:
        return (await session.execute(query)).unique().scalars().one()
    except NoResultFound:
        raise ObjectNotFoundError


async def get_total_rows(session: AsyncSession, query: Select) -> int:
    return (await session.execute(select(func.count()).select_from(query.subquery()))).scalars().one()
