from typing import TypeVar
from typing import Union

from src.databases import mongo
from src.databases import postgres

Session = TypeVar("Session", bound=Union[mongo.Session, postgres.Session])
