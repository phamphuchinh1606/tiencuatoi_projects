from fastapi import APIRouter

from app.api.dependencies import CurrentAdmin, CurrentUser, DbSession
from app.features.users.schemas import UserResponse, UserUpdate
from app.features.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    """Lấy thông tin người dùng hiện tại."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_me(payload: UserUpdate, current_user: CurrentUser, db: DbSession):
    """Cập nhật thông tin cá nhân."""
    service = UserService(db)
    return await service.update_user(current_user.id, payload)


@router.get("/", response_model=list[UserResponse])
async def list_users(db: DbSession, _: CurrentAdmin, skip: int = 0, limit: int = 20):
    """Lấy danh sách tất cả users (chỉ superuser)."""
    service = UserService(db)
    return await service.get_all(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: DbSession, _: CurrentAdmin):
    """Lấy thông tin user theo ID (chỉ superuser)."""
    service = UserService(db)
    return await service.get_by_id(user_id)
