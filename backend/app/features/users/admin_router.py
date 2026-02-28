"""
Admin quản lý Users — Dùng CurrentAdmin (token từ bảng admins).
Prefix: /admin/users
"""
from fastapi import APIRouter

from app.api.dependencies import CurrentAdmin, DbSession
from app.features.users.schemas import UserResponse, UserUpdate
from app.features.users.service import UserService

router = APIRouter(prefix="/users", tags=["🛡️ Admin — Users"])


@router.get("/", response_model=list[UserResponse], summary="Danh sách tất cả users")
async def list_all_users(db: DbSession, _: CurrentAdmin, skip: int = 0, limit: int = 50):
    """Admin xem toàn bộ users trong hệ thống."""
    return await UserService(db).get_all(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse, summary="Chi tiết một user")
async def get_user_detail(user_id: str, db: DbSession, _: CurrentAdmin):
    """Admin xem thông tin chi tiết bất kỳ user nào."""
    return await UserService(db).get_by_id(user_id)


@router.patch("/{user_id}", response_model=UserResponse, summary="Chỉnh sửa thông tin user")
async def update_user(user_id: str, payload: UserUpdate, db: DbSession, _: CurrentAdmin):
    """Admin chỉnh sửa thông tin của bất kỳ user nào."""
    return await UserService(db).update_user(user_id, payload)


@router.patch(
    "/{user_id}/toggle-active",
    response_model=UserResponse,
    summary="Kích hoạt / Vô hiệu hóa tài khoản user",
)
async def toggle_user_active(user_id: str, db: DbSession, _: CurrentAdmin):
    """Đảo trạng thái is_active của user (activate ↔ deactivate)."""
    return await UserService(db).toggle_active(user_id)


@router.delete("/{user_id}", status_code=204, summary="Xóa user")
async def delete_user(user_id: str, db: DbSession, _: CurrentAdmin):
    """Admin xóa vĩnh viễn một user."""
    await UserService(db).delete_user(user_id)
