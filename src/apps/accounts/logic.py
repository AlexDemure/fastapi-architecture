from typing import Optional

from src.apps.accounts import crud as account_crud
from src.schemas.accounts import AccountCreate, AccountData


async def get_account_by_id(account_id: int) -> Optional[AccountData]:
    account = await account_crud.get_account_by_id(account_id)
    return AccountData.from_orm(account) if account else None


async def create_account(account_create: AccountCreate) -> AccountData:
    account = await account_crud.create_account(account_create)
    return AccountData.from_orm(account)

