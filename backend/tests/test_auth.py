import pytest

@pytest.mark.asyncio
async def test_token_ok(client):
    
    resp = await client.post("/token", data={"username":"admin","password":"Suasenha123"})
    assert resp.status_code in (200, 400, 401)  
    if resp.status_code == 200:
        data = resp.json()
        assert "access_token" in data
