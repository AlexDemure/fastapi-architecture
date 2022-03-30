from typing import List

from fastapi import APIRouter, status

from src.api.const import USER_BASE_RESPONSES
from src.enums.base import BaseMessage
from src.enums.errors import AccountErrors
from src.logic import service_accounts
from src.schemas.accounts import AccountCreate, AccountData
from src.schemas.base import MessageErrorSchema

router = APIRouter()


@router.get(
    "/{account_id}",
    summary='Get account by id',
    status_code=status.HTTP_200_OK,
    response_model=AccountData,
    responses={
        **USER_BASE_RESPONSES,
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        status.HTTP_404_NOT_FOUND: {
            "model": MessageErrorSchema,
            "description": AccountErrors.account_not_found.docs_response
        },
    },
)
async def get_account_by_id_request(account_id: int) -> AccountData:
    """
    Get account by id.

    *Business-logic*:
        -  Account must be in database
    """

    return await service_accounts.get_account_by_id(account_id)


@router.post(
    "/",
    summary='Create account',
    status_code=status.HTTP_201_CREATED,
    response_model=AccountData,
    responses={
        status.HTTP_201_CREATED: {"description": BaseMessage.obj_is_created.value}
    },
)
async def create_account_request(account_create: AccountCreate) -> AccountData:
    """Create account."""

    return await service_accounts.create_account(account_create)


@router.get(
    "/",
    summary='Get list account',
    status_code=status.HTTP_200_OK,
    response_model=List[AccountData],
    responses={
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value}
    },
)
async def get_list_account_request() -> List[AccountData]:
    """Get list account."""

    return await service_accounts.get_list_account()
