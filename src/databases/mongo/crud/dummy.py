from src.databases.mongo import collections

from .base import CRUD


class Dummy(CRUD):
    collection = collections.Dummy
