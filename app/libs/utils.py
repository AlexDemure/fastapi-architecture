import traceback
from datetime import datetime


def get_traceback(exception: Exception) -> str:
    return "".join(line for line in (traceback.format_tb(exception.__traceback__)))


def get_elapsed(started_at: datetime) -> float:
    return round(datetime.utcnow().timestamp() - started_at.timestamp(), 4)
