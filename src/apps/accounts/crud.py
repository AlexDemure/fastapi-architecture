from src.apps.accounts.models import Account
from src.schemas.accounts import AccountCreate, AccountUpdate
from src.submodules.common.crud import CRUDBase


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    pass


accounts_crud = CRUDAccount(Account)
