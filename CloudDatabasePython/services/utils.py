from datetime import datetime

def today_id() -> str:
    """Return ISO date like '2025-01-14' for doc ID."""
    return datetime.now().strftime("%Y-%m-%d")


def start_of_month():
    """Return datetime object for the first day of the current month."""
    now = datetime.now()
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
