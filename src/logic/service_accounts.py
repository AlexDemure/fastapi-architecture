from typing import List, Optional

from fastapi import HTTPException, status

from src.crud.crud_accounts import crud_accounts
from src.enums.errors import AccountErrors
from src.schemas.accounts import AccountCreate, AccountData
from src.serializer import serialize_accounts


async def get_account_by_id(account_id: int) -> Optional[AccountData]:
    """Get account by id."""

    account = await crud_accounts.get(account_id)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=AccountErrors.account_not_found.value
        )

    return serialize_accounts.prepare_account_data(account)


async def create_account(account_create: AccountCreate) -> AccountData:
    """Create account."""

    account = await crud_accounts.create(account_create)
    return serialize_accounts.prepare_account_data(account)


async def get_list_account() -> List[AccountData]:
    """Get list account."""

    accounts = await crud_accounts.get_list()

    return [serialize_accounts.prepare_account_data(account) for account in accounts]
