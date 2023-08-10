from fastapi import APIRouter
from fastapi import Path
from fastapi import status

from app.core.tracing import TracingLevel
from app.core.tracing import context_tracing
from app.db.setup import async_session
from app.db.setup import commit
from app.enums.accounts import Permission
from app.exceptions.accounts import AccountNotFoundError
from app.logic.accounts import Account
from app.schemas.accounts import AccountResponse
from app.serializer.accounts import prepare_account
from app.utils import business_errors_to_swagger

router = APIRouter(prefix="/accounts")


@router.get(
    "/{account_id}",
    summary="Get account by id",
    status_code=status.HTTP_200_OK,
    responses=business_errors_to_swagger(AccountNotFoundError),
)
async def get_account_by_id_request(account_id: str = Path(...)) -> AccountResponse:
    with context_tracing(function_=get_account_by_id_request, level=TracingLevel.DEBUG) as tracing:
        tracing.set_tags(account_id=account_id)

        async with async_session() as session:
            account = await Account.get(session=session, account_id=account_id)

        return prepare_account(account)


@router.post(
    "/",
    summary="Create account",
    status_code=status.HTTP_201_CREATED,
)
async def create_account_request() -> AccountResponse:
    with context_tracing(function_=create_account_request, level=TracingLevel.INFO):
        async with async_session() as session:
            async with commit(session):
                account = await Account.create(session=session, permission=Permission.customer)

        return prepare_account(account)
