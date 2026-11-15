import asyncio

from sqlalchemy import select

from app.config import get_settings
from app.database import get_session_factory
from app.models.user import Role, User
from app.security import hash_password


async def seed_admin() -> None:
    settings = get_settings()

    if not settings.admin_email or not settings.admin_password:
        raise RuntimeError(
            "ADMIN_EMAIL и ADMIN_PASSWORD должны быть заданы в .env."
        )

    session_factory = get_session_factory()
    async with session_factory() as session:
        stmt = select(User).where(User.email == settings.admin_email)
        existing_user = await session.scalar(stmt)

        if existing_user:
            return

        admin_user = User(
            email=settings.admin_email,
            password_hash=hash_password(settings.admin_password),
            role=Role.admin,
        )
        session.add(admin_user)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed_admin())