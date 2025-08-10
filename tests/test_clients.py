import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_and_get_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
       
        resp = await ac.post("/clients/", json={"name": "Test User", "email": "testuser@example.com", "is_active": True})
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "testuser@example.com"

        client_id = data["id"]
        resp2 = await ac.get(f"/clients/{client_id}")
        assert resp2.status_code == 200
        assert resp2.json()["id"] == client_id
