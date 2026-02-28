"""
User Router Tổng Hợp — Gom tất cả endpoint dành cho User thông thường.
URL pattern: /api/v1/{resource}
"""
from fastapi import APIRouter

from app.features.auth.router import router as auth_router
from app.features.users.router import router as users_router

user_router = APIRouter()

# POST /api/v1/auth/register, /api/v1/auth/login — Public (không cần token)
user_router.include_router(auth_router)

# GET/PUT /api/v1/users/me — Thông tin cá nhân (yêu cầu User JWT)
user_router.include_router(users_router)
