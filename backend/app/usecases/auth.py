from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.security import hash_password, verify_password

class EmailTaken(Exception):
    pass

class InvalidCredentials(Exception):
    pass

async def register(session: AsyncSession, email: str, password: str) -> User:
    normalized_email = email.strip().lower()    
    stmt = select(User).where(User.email == normalized_email)
    existing_user = await session.scalar(stmt)
    if existing_user:
        raise EmailTaken("Пользователь с таким email уже существует")
    user = User(email=normalized_email, password_hash=hash_password(password))
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user

async def login(session: AsyncSession, email: str, password: str) -> User:
    normalized_email = email.strip().lower()
    stmt = select(User).where(User.email == normalized_email)
    user = await session.scalar(stmt)
    if (not user) or (not verify_password(password, user.password_hash)):
        raise InvalidCredentials("Неверный email или пароль")
    return user
    