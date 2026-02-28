import pytest
from unittest.mock import AsyncMock, patch
from app.repositories.implementations.user_repository import UserRepository


@pytest.mark.asyncio
async def test_get_by_email_returns_none_when_not_found(db_session):
    repo = UserRepository(db_session)
    result = await repo.get_by_email("notfound@example.com")
    assert result is None


@pytest.mark.asyncio
async def test_is_email_taken_returns_false(db_session):
    repo = UserRepository(db_session)
    result = await repo.is_email_taken("free@example.com")
    assert result is False
