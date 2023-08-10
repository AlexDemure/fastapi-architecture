from enum import Enum

import structlog


class Field(str, Enum):
    event = "event"
    levelname = "levelname"
    timestamp = "timestamp"
    facility = "facility"
    environment = "environment"

    def __call__(self, value) -> dict:
        return {self.name: value}


def _levelname_template(method: str, key: str, value: str) -> str:
    if method == "DEBUG":
        color = structlog.dev.BLUE
    elif method == "INFO":
        color = structlog.dev.RESET_ALL
    elif method == "WARNING":
        color = structlog.dev.YELLOW
    else:
        color = structlog.dev.RED

    return f"{color}{structlog.dev.BRIGHT}{value.upper()}{structlog.dev.RESET_ALL}:"


def _event_template(method: str, key: str, value: str) -> str:
    if method == "WARNING":
        color = structlog.dev.YELLOW
    elif method in ["ERROR", "CRITICAL"]:
        color = structlog.dev.RED
    else:
        color = structlog.dev.RESET_ALL

    return f"{color}{value}"


def _kwarg_template(method: str, key: str, value: str) -> str:
    return f"{structlog.dev.MAGENTA}{key}{structlog.dev.RESET_ALL}={structlog.dev.CYAN}{value}"


# GLOBAL SETTINGS FOR CONSOLE OUTPUT
FIELDS_SETTINGS = {
    Field.timestamp: dict(priority=0, template=lambda method, key, value: f"{structlog.dev.GREEN}{value}"),
    Field.levelname: dict(priority=1, template=_levelname_template),
    Field.event: dict(priority=2, template=_event_template),
    "kwarg": dict(priority=5, template=_kwarg_template),
}
