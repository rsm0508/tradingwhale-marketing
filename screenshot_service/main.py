from fastapi import FastAPI, Query
from starlette.responses import FileResponse
from playwright.async_api import async_playwright
import uuid, os, asyncio, json

TV_LAYOUT = os.getenv("TV_LAYOUT_ID")          # e.g. "XXXXXXXX"
PNG_DIR   = os.getenv("PNG_DIR", "/tmp/pngs")
os.makedirs(PNG_DIR, exist_ok=True)

app = FastAPI()

async def grab(symbol: str, interval: str) -> str:
    outfile = os.path.join(PNG_DIR, f"{uuid.uuid4()}.png")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(storage_state="cookies.json")
        page = await context.new_page()
        url = f"https://www.tradingview.com/chart/{TV_LAYOUT}/?symbol={symbol}&interval={interval}"
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(4000)  # let indicator paint
        await page.screenshot(path=outfile, full_page=False)
        await browser.close()
    return outfile

@app.get("/screenshot")
async def screenshot(symbol: str = Query(...), interval: str = Query(...)):
    path = await grab(symbol, interval)
    return FileResponse(path, media_type="image/png")
