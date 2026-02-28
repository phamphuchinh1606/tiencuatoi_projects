import time
import uuid

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware ghi log mỗi request/response."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        # Gắn request_id vào request state để dùng trong handler
        request.state.request_id = request_id

        response = await call_next(request)

        process_time = (time.perf_counter() - start_time) * 1000  # ms
        print(
            f"[{request_id}] {request.method} {request.url.path} "
            f"→ {response.status_code} ({process_time:.2f}ms)"
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        return response


def register_middlewares(app: FastAPI) -> None:
    """Đăng ký tất cả middleware tùy chỉnh."""
    app.add_middleware(LoggingMiddleware)
