from fastapi import APIRouter, WebSocket
import asyncio
import yfinance as yf

router = APIRouter()

async def get_price(symbol: str):
    ticker = yf.Ticker(symbol)
    price = ticker.history(period="1d")["Close"][-1]
    return price

@router.websocket("/ws/prices/{symbol}")
async def websocket_price(websocket: WebSocket, symbol: str):
    await websocket.accept()
    while True:
        price = await get_price(symbol)
        await websocket.send_json({"symbol": symbol, "price": price})
        await asyncio.sleep(5)
