from app.db.tables.accounts import Account
from app.schemas.accounts import AccountResponse


def prepare_account(account: Account) -> AccountResponse:
    return AccountResponse(
        id=account.id,
        created_at=account.created_at,
    )
