import enum
import json
from datetime import date
from datetime import datetime


class DatetimeAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, enum.Enum):
            return obj.value
        return json.JSONEncoder.default(self, obj)
