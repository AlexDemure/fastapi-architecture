from copy import deepcopy
from datetime import datetime
from typing import Any
from typing import Optional

from structlog.stdlib import BoundLogger

from .fields import Field


async def _ignore():
    """Function for exception handling."""
    return False


class BoundLoggerAdapter(BoundLogger):
    """Adapter for structlog и aiologger."""

    def _proxy_to_logger(self, method_name: str, event: Optional[str] = None, *args, **kwargs) -> Any:  # noqa:C901
        """
        Override parent method BoundLogger._proxy_to_logger

        Interface struclog: .debug(self, event: str | None = None, *args: Any, **kw: Any) -> Any:
        --- proxy_lo_logger ---
        Interface aiologger: .debug(self, msg, *args, **kwargs) -> Task:

        """

        if not kwargs.get(Field.timestamp, None):
            kwargs[Field.timestamp] = datetime.utcnow().isoformat()  # Add timestamp

        if not kwargs.get(Field.levelname, None):
            kwargs[Field.levelname] = method_name.upper()

        positional_args = list()

        if args:
            for arg in deepcopy(args):
                if isinstance(arg, dict):  # our Field enum
                    for key, value in arg.items():
                        kwargs[key] = value
                else:
                    positional_args.append(arg)

        if positional_args:
            kwargs["positional_args"] = positional_args

        try:
            _, kw = self._process_event(method_name=method_name, event=event, event_kw=kwargs)
            return getattr(self._logger, method_name)(msg=kw)
        except Exception:
            return _ignore()
