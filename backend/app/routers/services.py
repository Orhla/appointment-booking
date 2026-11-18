from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas.service import ServiceCreate, ServiceRead, ServicePublic
import app.usecases.services as svc
from app.dependencies import get_current_user, require_roles
from app.models.user import Role

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/", response_model=list[ServiceRead], dependencies=[Depends(get_current_user)])
async def get_services(session: AsyncSession = Depends(get_session)):
    return await svc.list_services(session)

@router.get("/public", response_model=list[ServicePublic])
async def get_public_services(session: AsyncSession = Depends(get_session)):
    return await svc.list_services(session)

@router.post("/", response_model=ServiceRead, status_code=201, dependencies=[Depends(require_roles(Role.master, Role.admin))])
async def post_service(
    data: ServiceCreate,
    session: AsyncSession = Depends(get_session),
):
    return await svc.create_service(session, data)