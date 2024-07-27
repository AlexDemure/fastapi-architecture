from typing import TypeVar

from src.databases.postgres.setup import Table

TableType = TypeVar("TableType", bound=Table)
