from enum import StrEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import CheckConstraint, DateTime, Index, String, func
from app.database import Base
from app.lib.consts import MAX_EMAIL_LENGTH

class Role(StrEnum):
    client = "client"
    master = "master"
    admin = "admin"


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(MAX_EMAIL_LENGTH))
    password_hash: Mapped[str]
    role: Mapped[Role] = mapped_column(
        String(32),
        default=Role.client,
        server_default=Role.client.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            f"role IN ({', '.join(repr(r.value) for r in Role)})",
            name="ck_users_role",
        ),
        Index("ix_users_email_lower", func.lower(email), unique=True),
    )