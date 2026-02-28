"""
Admin Router Tổng Hợp — Gom tất cả /admin/* endpoints.
Mọi endpoint ở đây đều yêu cầu Admin JWT (role=admin, từ bảng admins).

URL pattern: /api/v1/admin/{resource}
"""
from fastapi import APIRouter

from app.features.admin_auth.router import router as admin_auth_router
from app.features.users.admin_router import router as admin_users_router

admin_router = APIRouter(prefix="/admin")

# POST /api/v1/admin/auth/login — Đăng nhập admin (public, không cần token)
admin_router.include_router(admin_auth_router)

# /api/v1/admin/users/* — Quản lý users (yêu cầu Admin JWT)
admin_router.include_router(admin_users_router)
