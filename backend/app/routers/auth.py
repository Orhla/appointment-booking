from app.schemas.auth import RegisterRequest, LoginRequest, UserRead
from app.usecases.auth import register, login, EmailTaken, InvalidCredentials
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.config import get_settings
from app.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

def set_auth_cookie(response: Response, token: str) -> None:
    settings = get_settings()
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        max_age=settings.access_ttl_minutes * 60,
        path="/",
    )

@router.post("/register", response_model=UserRead, status_code=201)
async def post_register(data: RegisterRequest, response: Response, session: AsyncSession = Depends(get_session)):
    try:
        user = await register(session, data.email, data.password)
    except EmailTaken as e:
        raise HTTPException(status_code=409, detail=str(e))
    access_token = create_access_token(user_id=user.id, role=user.role)
    set_auth_cookie(response, access_token)
    return user

@router.post("/login", response_model=UserRead, status_code=200)
async def post_login(data: LoginRequest, response: Response, session: AsyncSession = Depends(get_session)):
    try:
        user = await login(session, data.email, data.password)
    except InvalidCredentials as e:
        raise HTTPException(status_code=401, detail=str(e))
    access_token = create_access_token(user_id=user.id, role=user.role)
    set_auth_cookie(response, access_token)
    return user

@router.post("/logout", status_code=204)
async def post_logout(response: Response):
    settings = get_settings()
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        path="/",
    )

@router.get("/me", response_model=UserRead)
async def get_me(current_user=Depends(get_current_user)):
    return current_user