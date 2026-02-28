from abc import abstractmethod
from typing import Optional

from app.models.user import User
from app.repositories.interfaces.base import IBaseRepository


class IUserRepository(IBaseRepository[User]):
    """
    Hợp đồng (Interface) riêng cho User Repository.
    Mở rộng thêm các method đặc thù của User ngoài CRUD cơ bản.
    """

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def is_email_taken(self, email: str) -> bool:
        raise NotImplementedError
