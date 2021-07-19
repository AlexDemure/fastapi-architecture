from datetime import datetime

from pydantic import BaseModel, constr


class AccountCreate(BaseModel):
    fullname: constr(min_length=1, max_length=255)


class AccountData(BaseModel):
    id: int
    fullname: constr(min_length=1, max_length=255)
    created_at: datetime

    class Config:
        orm_mode = True
