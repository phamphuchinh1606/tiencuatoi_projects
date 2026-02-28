"""
API V1 Router — Điểm vào chính, phân tách Admin và User.

Cấu trúc URL:
  /api/v1/auth/*          → Public (register, login user)
  /api/v1/users/*         → User routes (yêu cầu User JWT)
  /api/v1/orders/*        → User routes (yêu cầu User JWT)
  /api/v1/admin/auth/*    → Admin login (public)
  /api/v1/admin/users/*   → Admin routes (yêu cầu Admin JWT)
  /api/v1/admin/orders/*  → Admin routes (yêu cầu Admin JWT)
"""
from fastapi import APIRouter

from app.api.v1.routers.admin_router import admin_router
from app.api.v1.routers.user_router import user_router

api_router = APIRouter()

# ─── User Routes (prefix đã nằm trong từng feature router) ───────────────────
api_router.include_router(user_router)

# ─── Admin Routes (thêm prefix /admin, tất cả require Admin JWT) ─────────────
api_router.include_router(admin_router)
