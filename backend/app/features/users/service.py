from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.features.users.schemas import UserUpdate
from app.models.user import User
from app.repositories.implementations.user_repository import UserRepository


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def get_by_id(self, user_id: str) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found")
        return user

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.user_repo.get_all(skip=skip, limit=limit)

    async def update_user(self, user_id: str, payload: UserUpdate) -> User:
        update_data = payload.model_dump(exclude_unset=True)
        user = await self.user_repo.update(user_id, **update_data)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found")
        return user

    async def toggle_active(self, user_id: str) -> User:
        """Đảo trạng thái is_active: active → inactive hoặc ngược lại."""
        user = await self.get_by_id(user_id)
        updated = await self.user_repo.update(user_id, is_active=not user.is_active)
        return updated

    async def delete_user(self, user_id: str) -> None:
        deleted = await self.user_repo.delete(user_id)
        if not deleted:
            raise NotFoundException(f"User with id {user_id} not found")
