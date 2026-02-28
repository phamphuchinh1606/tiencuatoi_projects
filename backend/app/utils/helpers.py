import random
import string
from datetime import datetime, timezone


def generate_random_string(length: int = 8) -> str:
    """Tạo chuỗi ngẫu nhiên gồm chữ và số."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def format_datetime(dt: datetime, fmt: str = "%d/%m/%Y %H:%M") -> str:
    """Format datetime thành chuỗi theo định dạng Việt Nam."""
    return dt.strftime(fmt)


def utc_now() -> datetime:
    """Lấy thời điểm hiện tại theo UTC (timezone-aware)."""
    return datetime.now(timezone.utc)


def slugify(text: str) -> str:
    """Chuyển chuỗi thành slug (chỉ dùng ASCII cơ bản)."""
    return (
        text.lower()
        .strip()
        .replace(" ", "-")
        .replace("_", "-")
    )
