from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas.service import ServiceCreate, ServiceRead
import app.usecases.services as svc

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/", response_model=list[ServiceRead])
async def get_services(session: AsyncSession = Depends(get_session)):
    return await svc.list_services(session)


@router.post("/", response_model=ServiceRead, status_code=201)
async def post_service(
    data: ServiceCreate,
    session: AsyncSession = Depends(get_session),
):
    return await svc.create_service(session, data)