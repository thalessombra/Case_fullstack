import pytest

@pytest.mark.asyncio
async def test_asset_price_with_cache(monkeypatch, client):
    
    a = await client.post("/assets/", json={"symbol":"MSFT","name":"Microsoft"})
    assert a.status_code in (200,201), a.text

    
    from app.api.assets import get_asset_price_by_symbol 

    async def fake_fetch_price(symbol: str) -> float:
        return 123.45

    monkeypatch.setattr("app.api.assets.get_asset_price_by_symbol", fake_fetch_price)
   
    r1 = await client.get("/assets/MSFT/price")
    assert r1.status_code == 200
    assert r1.json()["price"] == 123.45

    
    r2 = await client.get("/assets/MSFT/price")
    assert r2.status_code == 200
    assert r2.json()["price"] == 123.45
