from enum import Enum

import structlog


class Field(str, Enum):
    event = "event"
    message = "message"

    level_name = "level_name"
    timestamp = "timestamp"
    level = "level"
    environment = "environment"
    facility = "facility"
    trace_id = "trace_id"
    span_id = "span_id"
    action_name = "action_name"

    elapsed = "elapsed"
    headers = "headers"
    request_data = "request_data"
    request_path = "request_path"
    url = "url"
    response_data = "response_data"

    exception_message = "exception_message"
    stack_trace = "stack_trace"

    def __call__(self, value) -> dict:
        return {self.value: value}


def wrapper_reset_color(string: str) -> str:
    return f"{structlog.dev.RESET_ALL}{string}{structlog.dev.RESET_ALL}"


def _levelname_template(method: str, key: str, value: str) -> str:
    if method == "DEBUG":
        color = structlog.dev.BLUE
    elif method == "INFO":
        color = structlog.dev.RESET_ALL
    elif method == "WARNING":
        color = structlog.dev.YELLOW
    else:
        color = structlog.dev.RED

    template = f"{color}{structlog.dev.BRIGHT}{value.upper()}:"

    return wrapper_reset_color(template)


def _event_template(method: str, key: str, value: str) -> str:
    if method == "WARNING":
        color = structlog.dev.YELLOW
    elif method in ["ERROR", "CRITICAL"]:
        color = structlog.dev.RED
    else:
        color = structlog.dev.RESET_ALL

    template = f"{color}{value}"

    return wrapper_reset_color(template)


def _timestamp_template(method: str, key: str, value: str) -> str:
    template = f"{structlog.dev.GREEN}{value}"

    return wrapper_reset_color(template)


def _kwarg_template(method: str, key: str, value: str) -> str:
    template = f"{structlog.dev.MAGENTA}{key}{structlog.dev.RESET_ALL}={structlog.dev.CYAN}{value}"

    return wrapper_reset_color(template)


# Стилистическая настройка лога для вывода в консоли
FIELDS_SETTINGS = {
    Field.timestamp: dict(priority=0, template=_timestamp_template),
    Field.level_name: dict(priority=1, template=_levelname_template),
    Field.event: dict(priority=2, template=_event_template),
    "kwarg": dict(priority=5, template=_kwarg_template),
}
