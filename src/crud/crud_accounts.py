from typing import List

from src.crud.base import CRUDBase
from src.models.accounts import Account
from src.schemas.accounts import AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):

    async def get_list(self) -> List[Account]:
        return await self.model.all()


crud_accounts = CRUDAccount(Account)
