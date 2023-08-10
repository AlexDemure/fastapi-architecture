from datetime import datetime

from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: str
    created_at: datetime
