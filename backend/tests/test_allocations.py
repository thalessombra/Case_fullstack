import pytest

pytestmark = pytest.mark.asyncio
async def test_allocation_crud(client):
    
    c = await client.post("/clients/", json={
        "name":"João",
        "email":"joao.alloc@example.com",
        "is_active": True,
        "password":"x"
    })
    assert c.status_code in (200,201), c.text
    client_id = c.json()["id"]
    
    a = await client.post("/assets/", json={
        "symbol":"AAPL",
        "name":"Apple Inc."
    })
    assert a.status_code in (200,201), a.text
    asset_id = a.json()["id"]
    
    alloc = await client.post("/allocations/", json={
        "client_id": client_id,
        "asset_id": asset_id,
        "qty": 10,
        "price": 150,
        "bought_at":"2025-08-01"
    })
    assert alloc.status_code in (200,201), alloc.text
    alloc_id = alloc.json()["id"]
    
    g = await client.get(f"/allocations/{alloc_id}")
    assert g.status_code == 200
    
    u = await client.put(f"/allocations/{alloc_id}", json={"qty": 12})
    assert u.status_code == 200
    assert u.json()["qty"] == 12
    
    d = await client.delete(f"/allocations/{alloc_id}")
    assert d.status_code in (200,204)
