from datetime import datetime, timezone


def utc_current_time():
    return datetime.now(tz=timezone.utc)