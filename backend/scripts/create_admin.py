#!/usr/bin/env python
"""
Script tạo tài khoản Admin đầu tiên.
Chạy trong Docker: docker compose exec api python scripts/create_admin.py
Chạy local:        python scripts/create_admin.py
"""
import asyncio
import sys
from pathlib import Path

# Thêm thư mục gốc vào path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.security import hash_password
from app.models.admin import Admin


async def create_admin(
    email: str,
    username: str,
    password: str,
    full_name: str | None = None,
) -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Kiểm tra email đã tồn tại chưa
        from sqlalchemy import select
        result = await session.execute(select(Admin).where(Admin.email == email))
        existing = result.scalar_one_or_none()

        if existing:
            print(f"❌ Admin với email '{email}' đã tồn tại!")
            return

        admin = Admin(
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=hash_password(password),
            is_active=True,
        )
        session.add(admin)
        await session.commit()
        await session.refresh(admin)

        print(f"✅ Tạo Admin thành công!")
        print(f"   ID       : {admin.id}")
        print(f"   Email    : {admin.email}")
        print(f"   Username : {admin.username}")
        print(f"   Full name: {admin.full_name}")

    await engine.dispose()


if __name__ == "__main__":
    import getpass

    print("═══════════════════════════════════════")
    print("   TienCuaToi — Tạo tài khoản Admin")
    print("═══════════════════════════════════════")

    email = input("Email: ").strip()
    username = input("Username: ").strip()
    full_name = input("Full name (bỏ trống nếu không có): ").strip() or None
    password = getpass.getpass("Password: ")
    confirm = getpass.getpass("Xác nhận password: ")

    if password != confirm:
        print("❌ Password không khớp!")
        sys.exit(1)

    if len(password) < 8:
        print("❌ Password phải ít nhất 8 ký tự!")
        sys.exit(1)

    asyncio.run(create_admin(email=email, username=username, password=password, full_name=full_name))
