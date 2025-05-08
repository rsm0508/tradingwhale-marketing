# monitor/kpi_tracker.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
BITLY_TOKEN = os.getenv("BITLY_TOKEN")
STRIPE_SECRET = os.getenv("STRIPE_SECRET")
BREVO_KEY = os.getenv("BREVO_KEY")
if not BITLY_TOKEN or not STRIPE_SECRET or not BREVO_KEY:
    raise EnvironmentError("Missing BITLY_TOKEN, STRIPE_SECRET, or BREVO_KEY in environment variables.")

def fetch_bitly_clicks():
    headers = {"Authorization": f"Bearer {BITLY_TOKEN}"}
    try:
        response = httpx.get("https://api-ssl.bitly.com/v4/bitlinks/YOUR_BITLINK_ID/clicks/summary", headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def fetch_stripe_mrr():
    headers = {"Authorization": f"Bearer {STRIPE_SECRET}"}
    try:
        response = httpx.get("https://api.stripe.com/v1/subscription_items", headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def fetch_brevo_unsubs():
    headers = {"api-key": BREVO_KEY}
    try:
        response = httpx.get("https://api.brevo.com/v3/contacts/statistics/unsubscribed", headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
