from abc import abstractmethod
from typing import Optional

from app.models.admin import Admin
from app.repositories.interfaces.base import IBaseRepository


class IAdminRepository(IBaseRepository[Admin]):
    """Hợp đồng (Interface) riêng cho Admin Repository."""

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Admin]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[Admin]:
        raise NotImplementedError

    @abstractmethod
    async def is_email_taken(self, email: str) -> bool:
        raise NotImplementedError
