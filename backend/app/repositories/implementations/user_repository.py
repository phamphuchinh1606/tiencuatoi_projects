from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.implementations.base import BaseRepository
from app.repositories.interfaces.user_repository import IUserRepository


class UserRepository(BaseRepository[User], IUserRepository):
    """
    Repository cụ thể cho User.
    Kế thừa BaseRepository (có CRUD) và IUserRepository (có contract).
    """

    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def is_email_taken(self, email: str) -> bool:
        user = await self.get_by_email(email)
        return user is not None
