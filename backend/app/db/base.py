# Import tất cả models vào đây để Alembic có thể phát hiện
# Giữ file này luôn được cập nhật khi thêm model mới

from app.db.session import engine  # noqa: F401
from app.models.base import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.admin import Admin  # noqa: F401
