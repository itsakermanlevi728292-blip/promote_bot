from datetime import datetime
from zoneinfo import ZoneInfo
from config import TIMEZONE

def format_timestamp(dt: datetime) -> str:
    tz = ZoneInfo(TIMEZONE)
    local = dt.astimezone(tz)
    return local.strftime("%d %b %Y • %I:%M:%S %p %Z")
