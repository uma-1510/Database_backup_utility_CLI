from datetime import datetime


def timestamp() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")
