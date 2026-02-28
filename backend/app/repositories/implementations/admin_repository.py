from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin import Admin
from app.repositories.implementations.base import BaseRepository
from app.repositories.interfaces.admin_repository import IAdminRepository


class AdminRepository(BaseRepository[Admin], IAdminRepository):
    """Repository thực thi cho Admin model."""

    def __init__(self, session: AsyncSession):
        super().__init__(model=Admin, session=session)

    async def get_by_email(self, email: str) -> Optional[Admin]:
        result = await self.session.execute(
            select(Admin).where(Admin.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[Admin]:
        result = await self.session.execute(
            select(Admin).where(Admin.username == username)
        )
        return result.scalar_one_or_none()

    async def is_email_taken(self, email: str) -> bool:
        return await self.get_by_email(email) is not None
