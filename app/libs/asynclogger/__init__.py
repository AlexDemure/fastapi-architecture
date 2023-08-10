import logging
import sys

import structlog
from aiologger import Logger
from aiologger.handlers.base import Handler
from structlog._config import BoundLoggerLazyProxy

from .adapter import BoundLoggerAdapter
from .handlers import ConsoleHandler
from .handlers import GraylogHandler
from .handlers import MockHandler

PROXY_LOGGER = Logger()


PROXY_LOGGER.add_handler(MockHandler())

structlog.configure(
    logger_factory=lambda: PROXY_LOGGER,
    wrapper_class=BoundLoggerAdapter,
    processors=[],
)


def console_handler(level: str = "DEBUG", fields: list[str] = None) -> ConsoleHandler:
    return ConsoleHandler(
        stream=sys.stdout,
        level=getattr(logging, level.upper()),
        formatter=None,
        filter=None,
        fields=fields,
    )


def graylog_handler(host: str, port: int, level: str = "DEBUG") -> GraylogHandler:
    return GraylogHandler(host=host, port=port, level=getattr(logging, level.upper()))


def add_handler(handler: Handler) -> None:
    PROXY_LOGGER.add_handler(handler)


def get_logger(logger: BoundLoggerLazyProxy = None, **kwargs) -> BoundLoggerLazyProxy:
    initial_values = dict()

    if logger:
        initial_values.update(**logger._initial_values)

    initial_values.update(**kwargs)

    return structlog.get_logger(**initial_values)
