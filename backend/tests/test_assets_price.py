import pytest

@pytest.mark.asyncio
async def test_asset_price_with_cache(monkeypatch, client):
    a = await client.post("/assets/", json={"ticker": "MSFT", "name": "Microsoft"})
    assert a.status_code in (200, 201), a.text

    
    def fake_sync_fetch_price(sym: str):
        return 123.45
    
    monkeypatch.setattr("app.api.assets._sync_fetch_price", fake_sync_fetch_price)

    
    r1 = await client.get("/assets/symbol/MSFT/price")
    assert r1.status_code == 200
    assert r1.json()["price"] == 123.45
    assert r1.json()["source"] in ("yfinance", "cache")  
    
    r2 = await client.get("/assets/symbol/MSFT/price")
    assert r2.status_code == 200
    assert r2.json()["price"] == 123.45
