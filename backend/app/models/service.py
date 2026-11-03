from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric
from app.database import Base
from decimal import Decimal

class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    duration_min: Mapped[int]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))