from copy import deepcopy
from typing import Optional

from aiologger.handlers.base import Handler
from aiologger.handlers.streams import AsyncStreamHandler as _AsyncStreamHandler
from aiologger.records import LogRecord

from .fields import FIELDS_SETTINGS

MAX_LENGTH_FIELD = 27648


class MockHandler(Handler):
    def initialized(self):
        pass

    async def close(self) -> None:
        pass

    async def emit(self, *args, **kwargs) -> None:
        pass


class ConsoleHandler(_AsyncStreamHandler):
    fields: Optional[list[str]] = None

    def __init__(self, fields: Optional[list[str]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields = fields

    def make_log(self, copy: LogRecord) -> str:
        context: dict = copy.msg

        if self.fields:  # Урезаем контекст если передан список ключей
            context = {k: v for k, v in context.items() if k in self.fields}

        fields = list()

        for key, value in context.items():
            settings = FIELDS_SETTINGS.get(key, FIELDS_SETTINGS["kwarg"])  # Получаем настройки по каждому ключу

            fields.append(dict(priority=settings["priority"], string=settings["template"](copy.levelname, key, value)))

        fields.sort(key=lambda item: item["priority"])  # Сортируем объекты по приоритету

        return "\u0020".join(item["string"] for item in fields)  # Формируем строку

    async def handle(self, record: LogRecord) -> bool:
        copy = deepcopy(record)

        copy.msg = self.make_log(copy)

        return await super().handle(copy)
