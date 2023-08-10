import json
from contextlib import asynccontextmanager
from functools import partial
from functools import wraps

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.serializer import DatetimeAwareJSONEncoder
from app.core.settings import config

custom_serializer = partial(json.dumps, cls=DatetimeAwareJSONEncoder, ensure_ascii=False)


engine = create_async_engine(
    config.POSTGRES_URI,
    echo=config.POSTGRES_ECHO,
    future=True,
    isolation_level="READ COMMITTED",  # Не изменять
    json_serializer=custom_serializer,
    pool_pre_ping=True,
    pool_timeout=1,
    pool_size=10,
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=True)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)


def get_session(function_):
    @wraps(function_)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            value = await function_(session=session, *args, **kwargs)
        return value

    return wrapper


@asynccontextmanager
async def commit(session: AsyncSession) -> AsyncSession:
    try:
        if session.in_transaction():
            yield session

        else:
            async with session.begin():
                yield session

        await session.commit()

    except Exception as e:
        await session.rollback()
        raise e
