import pytest

@pytest.mark.asyncio
async def test_create_and_list_clients(client):
    
    login_payload = {
        "username": "admin@empresa.com",  
        "password": "Suasenha123"      
    }
    login_resp = await client.post("/auth/jwt/login", data=login_payload)
    assert login_resp.status_code == 200, login_resp.text
    token = login_resp.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    
    payload = {
        "name": "Cliente Teste",
        "email": "cliente.teste@example.com",
        "is_active": True,
        "password": "Senha123!"
    }
    r = await client.post("/clients/", json=payload, headers=headers)
    assert r.status_code in (200, 201), r.text
    data = r.json()
    assert data["email"] == payload["email"]
    
    r2 = await client.get("/clients/", headers=headers)
    assert r2.status_code == 200
    lst = r2.json()
    assert any(c["email"] == payload["email"] for c in lst)
