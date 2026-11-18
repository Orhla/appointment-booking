import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from app.models.user import Role

import jwt
from pwdlib import PasswordHash

from app.config import get_settings

_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return _hasher.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return _hasher.verify(password, password_hash)

def create_access_token(user_id: int, role: Role) -> str:
    s = get_settings()
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "role": role.value,
        "iat": now,
        "exp": now + timedelta(minutes=s.access_ttl_minutes),
    }
    return jwt.encode(payload, s.jwt_secret, algorithm=s.jwt_algorithm)

def decode_access_token(token: str) -> tuple[int, Role]:
    s = get_settings()

    payload = jwt.decode(token, s.jwt_secret, algorithms=[s.jwt_algorithm])
    sub = payload.get("sub")
    if not sub:
        raise jwt.InvalidTokenError("Отсутствует ключ sub")
    raw_role = payload.get("role")
    if not raw_role:
        raise jwt.InvalidTokenError("Отсутствует ключ role")
        
    try:
        role = Role(raw_role)
    except ValueError as e:
        raise jwt.InvalidTokenError("Некорректное значение role")
    
    return (int(sub), role)


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(32)

def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()