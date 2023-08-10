import json
import socket
from copy import deepcopy

import structlog
from aiologger.handlers.base import Handler
from aiologger.handlers.streams import AsyncStreamHandler as _AsyncStreamHandler
from aiologger.levels import LogLevel
from aiologger.records import LogRecord
from graypy.handler import GELFUDPHandler as _GELFUDPHandler

from .fields import FIELDS_SETTINGS


class MockHandler(Handler):
    def initialized(self):
        pass

    async def close(self) -> None:
        pass

    async def emit(self, *args, **kwargs) -> None:
        pass


class ConsoleHandler(_AsyncStreamHandler):
    """Extend aiologger.AsyncStreamHandler to be able to customize log"""

    fields: list[str] = None

    def __init__(self, fields: list[str] = None, *args, **kwargs):
        """fields: Fields that will be displayed in the console for example: [event, timestamp]."""

        super().__init__(*args, **kwargs)

        self.fields = fields

    def make_log(self, copy: LogRecord) -> str:
        """Generating a string for output to the console."""

        context: dict = copy.msg

        if self.fields:
            context = {k: v for k, v in context.items() if k in self.fields}

        fields = list()

        for key, value in context.items():
            settings = FIELDS_SETTINGS.get(key, FIELDS_SETTINGS["kwarg"])  # Getting settings for each key

            fields.append(dict(priority=settings["priority"], string=settings["template"](copy.levelname, key, value)))

        fields.sort(key=lambda item: item["priority"])  # Sort objects by priority

        log = f"{structlog.dev.RESET_ALL}\u0020".join(item["string"] for item in fields)  # Forming log

        return f"{structlog.dev.RESET_ALL}{log}{structlog.dev.RESET_ALL}"  # Clear formatting

    async def handle(self, record: LogRecord) -> bool:
        """
        Override Handler.handle

        Call from aiologger.Logger.call_handlers.
        """

        copy = deepcopy(record)

        copy.msg = self.make_log(copy)

        return await super().handle(copy)


class GraylogHandler(Handler):
    """Handler for sending logs to Graylog via UDP"""

    handler: _GELFUDPHandler = None

    def __init__(self, host: str, port: int, level: int) -> None:
        super().__init__(level=LogLevel(level))

        self.handler = _GELFUDPHandler(host=host, port=port)

    def initialized(self):
        pass

    async def close(self) -> None:
        pass

    @classmethod
    def make_log(cls, copy: LogRecord) -> bytes:
        """
        Generation of GELF messages in Graylog.

        Does not accept a message if the format in the fields is violated:
            - level: int
            - message: str
        Automatically generates
            - timestamp - which cannot be overridden
            - message - takes as far as I understand from short_message
        """

        gelf_message = {
            "version": "1.1",
            "host": socket.getfqdn(),
            "short_message": json.dumps(copy.msg["event"], ensure_ascii=False),
            **{k: str(v) for k, v in copy.msg.items()},
        }

        return json.dumps(gelf_message).encode("utf-8")

    async def emit(self, record: LogRecord) -> None:
        """Override Handler.emit for sending log to Graylog."""

        copy = deepcopy(record)

        self.handler.send(self.make_log(copy))
