from app.db.crud.base import CRUDBase
from app.db.tables.accounts import Account as _Account


class Account(CRUDBase):
    table = _Account
