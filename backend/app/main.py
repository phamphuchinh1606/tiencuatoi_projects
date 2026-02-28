from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api_router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.middleware import register_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: khởi tạo kết nối DB, cache, v.v.
    print("🚀 Application starting up...")
    yield
    # Shutdown: đóng kết nối
    print("🛑 Application shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # Đăng ký CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Đăng ký Middleware tùy chỉnh
    register_middlewares(app)

    # Đăng ký Exception Handlers toàn cục
    register_exception_handlers(app)

    # Mount API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_app()
