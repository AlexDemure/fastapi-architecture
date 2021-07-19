from fastapi import APIRouter, HTTPException, status

from src.apps.accounts import logic as account_logic
from src.enums.accounts import AccountErrors
from src.schemas.accounts import AccountCreate, AccountData
from src.submodules.common.responses import base_responses

router = APIRouter()


@router.get(
    "/{account_id}",
    responses=base_responses,
)
async def read_user_me(account_id: int) -> AccountData:
    account = await account_logic.get_account_by_id(account_id)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=AccountErrors.account_not_found.value
        )

    return account


@router.post("/")
async def create_account(account_create: AccountCreate) -> AccountData:
    return await account_logic.create_account(account_create)
