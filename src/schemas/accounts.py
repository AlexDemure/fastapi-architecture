from datetime import datetime

from pydantic import BaseModel, constr


class AccountBase(BaseModel):
    fullname: constr(min_length=1, max_length=255)


class AccountCreate(AccountBase):
    pass


class AccountUpdate(AccountBase):
    pass


class AccountData(AccountBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
