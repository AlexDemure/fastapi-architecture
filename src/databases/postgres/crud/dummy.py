from sqlalchemy import select

from src.databases.postgres import tables
from src.databases.postgres.setup import AsyncSession
from src.framework.i18n import Locale

from .base import CRUD
from .base import get_list


class Dummy(CRUD):
    table = tables.Dummy
