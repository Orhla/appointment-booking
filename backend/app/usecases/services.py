from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.service import Service
from app.schemas.service import ServiceCreate


async def list_services(session: AsyncSession) -> list[Service]:
    stmt = select(Service)
    result = await session.scalars(stmt)
    return result.all()


async def create_service(session: AsyncSession, data: ServiceCreate) -> Service:
    db_service = Service(**data.model_dump())
    session.add(db_service)
    await session.commit()
    await session.flush()
    await session.refresh(db_service)
    return db_service