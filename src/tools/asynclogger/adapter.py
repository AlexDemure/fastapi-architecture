from copy import deepcopy
from datetime import datetime
from typing import Any
from typing import Optional

from structlog.stdlib import BoundLogger

from .fields import Field


async def _ignore():
    return False


class BoundLoggerAdapter(BoundLogger):
    def _proxy_to_logger(self, method_name: str, event: Optional[str] = None, *args, **kwargs) -> Any:  # noqa:C901
        if not kwargs.get(Field.timestamp.value, None):
            kwargs[Field.timestamp.value] = datetime.utcnow().isoformat()  # Добавление даты лога

        if not kwargs.get(Field.level_name.value, None):
            kwargs[Field.level_name.value] = method_name.upper()

        positional_args = list()

        if args:
            for arg in deepcopy(args):
                if isinstance(arg, dict):
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
