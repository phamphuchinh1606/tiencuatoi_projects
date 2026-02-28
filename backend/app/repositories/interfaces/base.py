from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class IBaseRepository(ABC, Generic[ModelType]):
    """
    Hợp đồng (Interface) CRUD chung cho tất cả Repository.
    id dùng str (UUID lưu dạng CHAR(36) trên MySQL).
    """

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, **kwargs) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: str, **kwargs) -> Optional[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: str) -> bool:
        raise NotImplementedError
