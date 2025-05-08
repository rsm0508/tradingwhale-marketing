# bots/facebook_bot.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")
if not FB_PAGE_ID or not FB_PAGE_TOKEN:
    raise EnvironmentError("Missing FB_PAGE_ID or FB_PAGE_TOKEN in environment variables.")

def post_to_facebook(caption: str, image_path: str):
    url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos"
    with open(image_path, 'rb') as img:
        files = {'source': img}
        data = {
            'caption': caption,
            'access_token': FB_PAGE_TOKEN
        }
        response = requests.post(url, files=files, data=data)
        return response.status_code, response.json()

# Example use (for local testing)
if __name__ == "__main__":
    status, result = post_to_facebook(
        "New BTC signal just hit. See it live → https://tradingwhale.io",
        "./sample_chart.png"
    )
    print(status, result)
