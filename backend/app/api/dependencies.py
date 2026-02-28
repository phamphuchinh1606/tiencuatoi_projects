from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_token
from app.db.session import get_db
from app.models.admin import Admin
from app.models.user import User
from app.repositories.implementations.admin_repository import AdminRepository
from app.repositories.implementations.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


# ─── User Authentication ──────────────────────────────────────────────────────

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency xác thực JWT user token (role='user').
    Dùng cho tất cả route của user thông thường.
    """
    if not credentials:
        raise UnauthorizedException("Authorization header is missing")

    try:
        payload = decode_token(credentials.credentials)
    except ValueError:
        raise UnauthorizedException("Invalid or expired token")

    # Kiểm tra đây phải là user token
    if payload.get("role") != "user":
        raise UnauthorizedException("This endpoint requires a user token")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Token payload is invalid")

    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)

    if not user:
        raise UnauthorizedException("User not found")

    if not user.is_active:
        raise UnauthorizedException("User account is inactive")

    return user


# ─── Admin Authentication ─────────────────────────────────────────────────────

async def get_current_admin(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: AsyncSession = Depends(get_db),
) -> Admin:
    """
    Dependency xác thực JWT admin token (role='admin').
    Tra cứu bảng 'admins' — hoàn toàn tách biệt với bảng 'users'.
    Dùng cho tất cả route /api/v1/admin/...
    """
    if not credentials:
        raise UnauthorizedException("Authorization header is missing")

    try:
        payload = decode_token(credentials.credentials)
    except ValueError:
        raise UnauthorizedException("Invalid or expired admin token")

    # Kiểm tra đây phải là admin token
    if payload.get("role") != "admin":
        raise ForbiddenException("This endpoint requires an admin token")

    admin_id = payload.get("sub")
    if not admin_id:
        raise UnauthorizedException("Admin token payload is invalid")

    # Tra cứu bảng admins (không phải bảng users!)
    repo = AdminRepository(db)
    admin = await repo.get_by_id(admin_id)

    if not admin:
        raise UnauthorizedException("Admin account not found")

    if not admin.is_active:
        raise UnauthorizedException("Admin account is inactive")

    return admin


# ─── Type Aliases ─────────────────────────────────────────────────────────────

# Dùng trong User routes
CurrentUser = Annotated[User, Depends(get_current_user)]

# Dùng trong Admin routes (/api/v1/admin/...)
CurrentAdmin = Annotated[Admin, Depends(get_current_admin)]

# DB Session
DbSession = Annotated[AsyncSession, Depends(get_db)]
