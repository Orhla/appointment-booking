import pytest
from app.usecases.services import create_service, list_services
from app.schemas.service import ServiceCreate

@pytest.mark.asyncio
async def test_create_and_list(session):
    data = ServiceCreate(name="Стрижка", duration_min=60, price=2000)
    created = await create_service(session, data)
    await session.commit()

    services = await list_services(session)
    assert len(services) == 1
    assert services[0].name == "Стрижка"