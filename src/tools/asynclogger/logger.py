import logging
import sys
from typing import Optional

import structlog
from aiologger import Logger
from aiologger.handlers.base import Handler
from structlog._config import BoundLoggerLazyProxy

from .adapter import BoundLoggerAdapter
from .handlers import ConsoleHandler
from .handlers import MockHandler

PROXY_LOGGER = Logger()

PROXY_LOGGER.add_handler(MockHandler())

structlog.configure(
    logger_factory=lambda: PROXY_LOGGER,
    wrapper_class=BoundLoggerAdapter,
    processors=[],
)


def console_handler(level: str = "DEBUG", fields: Optional[list[str]] = None) -> ConsoleHandler:
    return ConsoleHandler(
        stream=sys.stdout,
        level=getattr(logging, level.upper()),
        formatter=None,
        filter=None,
        fields=fields,
    )


def add_handler(handler: Handler) -> None:
    [PROXY_LOGGER.remove_handler(handler) for handler in PROXY_LOGGER.handlers if isinstance(handler, MockHandler)]
    PROXY_LOGGER.add_handler(handler)


def get_logger(**kwargs) -> BoundLoggerLazyProxy:
    return structlog.get_logger(**kwargs)
