from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.admin_auth.schemas import AdminLoginRequest, AdminLoginResponse
from app.features.admin_auth.service import AdminAuthService

router = APIRouter(prefix="/auth", tags=["🔐 Admin — Auth"])


@router.post(
    "/login",
    response_model=AdminLoginResponse,
    summary="Đăng nhập Admin",
    description=(
        "Đăng nhập bằng tài khoản Admin (từ bảng `admins`, "
        "hoàn toàn tách biệt với tài khoản User). "
        "Trả về JWT token với `role=admin`."
    ),
)
async def admin_login(
    payload: AdminLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AdminAuthService(db)
    return await service.login(payload)
