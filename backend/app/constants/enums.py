from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class OrderStatusMessage(str, Enum):
    PENDING = "Chờ xác nhận"
    PROCESSING = "Đang xử lý"
    COMPLETED = "Hoàn thành"
    CANCELLED = "Đã hủy"


# Thông báo tĩnh
class Message:
    SUCCESS = "Thao tác thành công"
    CREATED = "Tạo mới thành công"
    UPDATED = "Cập nhật thành công"
    DELETED = "Xóa thành công"
    NOT_FOUND = "Không tìm thấy dữ liệu"
    UNAUTHORIZED = "Bạn chưa đăng nhập"
    FORBIDDEN = "Bạn không có quyền thực hiện thao tác này"
