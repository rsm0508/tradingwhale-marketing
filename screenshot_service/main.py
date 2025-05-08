from fastapi import FastAPI, Query
from starlette.responses import JSONResponse
from playwright.async_api import async_playwright
import uuid, os, sys

# Ensure the current directory is in sys.path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from marketing_agent import generate_blurb

TV_LAYOUT = os.getenv("TV_LAYOUT_ID")
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
        await page.wait_for_timeout(4000)
        await page.screenshot(path=outfile, full_page=False)
        await browser.close()
    return outfile

@app.get("/screenshot")
async def screenshot(symbol: str = Query(...), interval: str = Query(...)):
    try:
        image_path = await grab(symbol, interval)
        blurb = generate_blurb(symbol, interval)
        return JSONResponse({"image_path": image_path, "blurb": blurb})
    except Exception as e:
        return JSONResponse({"error": str(e)})

@app.get("/blurb")
async def get_blurb(
    symbol: str = Query(...),
    interval: str = Query(...),
    signal_type: str = Query("buy")
):
    blurb = generate_blurb(symbol, interval, signal_type)
    return {"blurb": blurb}