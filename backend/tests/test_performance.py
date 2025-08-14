import pytest

@pytest.mark.asyncio
async def test_client_performance(client):
    
    c = await client.post("/clients/", json={
        "name":"Perf",
        "email":"perf@example.com",
        "is_active": True,
        "password":"x"
    })
    assert c.status_code in (200,201)
    cid = c.json()["id"]

    
    r = await client.get(f"/clients/{cid}/performance")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
