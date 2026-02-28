from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedException
from app.core.security import create_admin_access_token, verify_password
from app.features.admin_auth.schemas import AdminLoginRequest, AdminLoginResponse
from app.repositories.implementations.admin_repository import AdminRepository


class AdminAuthService:
    def __init__(self, db: AsyncSession):
        self.admin_repo = AdminRepository(db)

    async def login(self, payload: AdminLoginRequest) -> AdminLoginResponse:
        """
        Xác thực thông tin đăng nhập admin từ bảng 'admins'.
        Trả về JWT token với role='admin'.
        """
        admin = await self.admin_repo.get_by_email(payload.email)

        if not admin or not verify_password(payload.password, admin.hashed_password):
            raise UnauthorizedException("Invalid email or password")

        if not admin.is_active:
            raise UnauthorizedException("Admin account is inactive")

        access_token = create_admin_access_token(admin.id)

        return AdminLoginResponse(
            access_token=access_token,
            admin_id=admin.id,
            username=admin.username,
            full_name=admin.full_name,
        )
