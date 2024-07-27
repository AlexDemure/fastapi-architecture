import enum
import json
import traceback
from datetime import date
from datetime import datetime
from decimal import Decimal


class DatetimeAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, enum.Enum):
            return obj.value
        elif isinstance(obj, Decimal):
            return str(obj)
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)


def get_traceback(exception: Exception) -> str:
    return "".join(line for line in (traceback.format_tb(exception.__traceback__)))


def get_elapsed(started_at: datetime) -> float:
    return (datetime.utcnow() - started_at).total_seconds()
