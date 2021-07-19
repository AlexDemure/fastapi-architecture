from fastapi import APIRouter, HTTPException, status

from src.apps.accounts import logic as account_logic
from src.schemas.accounts import AccountCreate, AccountData

router = APIRouter()


@router.get("/{account_id}")
async def read_user_me(account_id: int) -> AccountData:
    account = await account_logic.get_account_by_id(account_id)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account is not found"
        )

    return account


@router.post("/")
async def create_account(account_create: AccountCreate) -> AccountData:
    return await account_logic.create_account(account_create)
