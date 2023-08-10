from datetime import datetime

from app.core.tracing import Tracing
from app.core.tracing import TracingLevel
from app.core.tracing import decorator_tracing
from app.db.crud.accounts import Account as CRUDAccount
from app.db.setup import AsyncSession
from app.db.tables.accounts import Account as TableAccount
from app.exceptions.accounts import AccountNotFoundError
from app.exceptions.crud import ObjectNotFoundError


class Account:
    crud = CRUDAccount

    @classmethod
    @decorator_tracing(return_tracing=False, level=TracingLevel.DEBUG)
    async def get(cls, session: AsyncSession, account_id: str) -> TableAccount:
        try:
            return await cls.crud.get(session, "id", account_id)
        except ObjectNotFoundError:
            raise AccountNotFoundError

    @classmethod
    @decorator_tracing(return_tracing=True, level=TracingLevel.DEBUG)
    async def create(cls, tracing: Tracing, session: AsyncSession, **kwargs) -> TableAccount:
        created_fields = dict(created_at=datetime.utcnow(), **kwargs)

        account = await cls.crud.create(session, **created_fields)

        tracing.object_created(cls.__name__, account_id=account.id, created_fields=created_fields)

        return account
