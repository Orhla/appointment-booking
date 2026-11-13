from app.usecases.services import create_service, list_services
from app.schemas.service import ServiceCreate

async def test_create_and_list(session):
    data = ServiceCreate(name="Стрижка", duration_min=60, price=2000)
    await create_service(session, data)

    services = await list_services(session)
    assert len(services) == 1
    assert services[0].name == "Стрижка"


async def test_create_and_list_via_api(client):
    payload = {"name": "Стрижка", "duration_min": 60, "price": 2000}

    response = await client.post("/services/", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created == {"id": created["id"], **payload}

    response = await client.get("/services/")
    assert response.status_code == 200
    assert response.json() == [created]