from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ENUM

from app.db.setup import Base
from app.enums.accounts import Permission
from app.utils import new_uuid


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String(36), primary_key=True, default=new_uuid)
    permission = Column(ENUM(Permission), nullable=False)
    created_at = Column(DateTime(), nullable=False)
