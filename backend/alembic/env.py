import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

# Import tất cả models để Alembic có thể autogenerate
from app.db.base import Base  # noqa: F401
from app.core.config import settings

# Alembic Config object - truy cập .ini
config = context.config

# Đọc cấu hình logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Gán metadata của các models vào Alembic để autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Chạy migration ở chế độ 'offline' (không cần kết nối DB)."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Chạy migration ở chế độ async."""
    engine = create_async_engine(settings.DATABASE_URL)

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()


def run_migrations_online() -> None:
    """Chạy migration ở chế độ 'online' (kết nối DB thật)."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
