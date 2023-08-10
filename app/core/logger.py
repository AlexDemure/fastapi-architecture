from app.core.settings import config
from app.libs.asynclogger import add_handler
from app.libs.asynclogger import console_handler
from app.libs.asynclogger import get_logger
from app.libs.asynclogger import graylog_handler
from app.libs.asynclogger.fields import Field

if config.LOGGER_CONSOLE:
    add_handler(console_handler(level=config.LOGGER_CONSOLE_LEVEL))

if config.LOGGER_GRAYLOG:
    add_handler(
        graylog_handler(
            host=config.LOGGER_GRAYLOG_HOST,
            port=config.LOGGER_GRAYLOG_PORT,
            level=config.LOGGER_GRAYLOG_LEVEL,
        )
    )


_initial_values = {Field.facility: config.PROJECT_NAME, Field.environment: config.ENV}

logger = get_logger(**_initial_values)
