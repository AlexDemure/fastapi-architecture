from sqlalchemy import BigInteger
from sqlalchemy import Column

from .base import Table


class Dummy(Table):
    __tablename__ = "dummy"

    id = Column(BigInteger, primary_key=True)
