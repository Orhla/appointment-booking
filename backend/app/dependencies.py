from fastapi import Cookie, HTTPException, Depends
from app.models.user import User, Role
from app.security import decode_access_token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session

async def get_current_user(access_token: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_session)) -> User:
    if not access_token:
        raise HTTPException(status_code=401, detail="Отсутствует access token")
    try:
        user_id, role = decode_access_token(access_token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Неверный или недействительный токен",
        )
    stmt = select(User).where(User.id == user_id)
    user = await session.scalar(stmt)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user

def require_roles(*roles: Role):
    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail="Недостаточно прав",
            )
        return current_user

    return role_checker