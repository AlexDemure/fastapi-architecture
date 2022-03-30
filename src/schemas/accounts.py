from datetime import datetime

from pydantic import BaseModel, Field

from src.enums.accounts import AccountType


class AccountBase(BaseModel):
    fullname: str = Field(min_length=1, max_length=255)
    account_type: AccountType


class AccountCreate(AccountBase):
    pass


class AccountUpdate(AccountBase):
    pass


class AccountData(AccountBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
