from src.models.accounts import Account
from src.schemas.accounts import AccountData


def prepare_account_data(account: Account) -> AccountData:
    return AccountData.from_orm(account)
