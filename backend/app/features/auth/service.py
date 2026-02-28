from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestException, ConflictException, UnauthorizedException
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.features.auth.schemas import LoginRequest, LoginResponse, RegisterRequest
from app.repositories.implementations.user_repository import UserRepository


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register(self, payload: RegisterRequest) -> LoginResponse:
        # Kiểm tra email đã tồn tại chưa
        if await self.user_repo.is_email_taken(payload.email):
            raise ConflictException("Email already registered")

        # Kiểm tra username đã tồn tại chưa
        if await self.user_repo.get_by_username(payload.username):
            raise ConflictException("Username already taken")

        # Tạo user mới
        user = await self.user_repo.create(
            email=payload.email,
            username=payload.username,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
        )

        return LoginResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def login(self, payload: LoginRequest) -> LoginResponse:
        user = await self.user_repo.get_by_email(payload.email)

        if not user or not verify_password(payload.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedException("Account is inactive")

        return LoginResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )
