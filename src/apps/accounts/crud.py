from typing import Optional

from src.apps.accounts.models import Account
from src.schemas.accounts import AccountCreate


async def get_account_by_id(account_id: int) -> Optional[Account]:
    return await Account.filter(id=account_id).first()


async def create_account(account_create: AccountCreate) -> Account:
    return await Account.create(**account_create.dict())
