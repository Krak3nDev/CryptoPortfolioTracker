from datetime import datetime, timedelta, timezone


def get_now_and_expiration(expire_minutes: int) -> tuple[datetime, datetime]:
    now = datetime.now(timezone.utc)
    expiration_time = now + timedelta(minutes=expire_minutes)
    return now, expiration_time
