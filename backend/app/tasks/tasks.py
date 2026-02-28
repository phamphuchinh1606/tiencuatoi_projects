# Celery tasks - Chạy tác vụ ngầm (Background Jobs)
# Tương tự Laravel Jobs / Queues

# from celery import Celery
# from app.core.config import settings

# celery_app = Celery(
#     "tasks",
#     broker=settings.CELERY_BROKER_URL,
#     backend=settings.CELERY_RESULT_BACKEND,
# )

# @celery_app.task
# def send_welcome_email(user_email: str) -> None:
#     """Gửi email chào mừng sau khi đăng ký."""
#     pass

# @celery_app.task
# def process_order(order_id: str) -> None:
#     """Xử lý đơn hàng ngầm sau khi tạo."""
#     pass
