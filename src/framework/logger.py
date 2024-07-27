from src.tools.asynclogger import Field
from src.tools.asynclogger import add_handler
from src.tools.asynclogger import console_handler
from src.tools.asynclogger import get_logger

from .settings import settings

if settings.LOGGER_CONSOLE:
    add_handler(console_handler(level=settings.LOGGER_CONSOLE_LEVEL))


_initial_values = {
    Field.facility.value: settings.SERVER_NAME,
    Field.environment.value: settings.SERVER_ENV,
}


logger = get_logger(**_initial_values)
