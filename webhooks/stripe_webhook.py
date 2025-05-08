# webhooks/stripe_webhook.py
import os
import stripe
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
if not STRIPE_WEBHOOK_SECRET:
    raise EnvironmentError("Missing STRIPE_WEBHOOK_SECRET in environment variables.")

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    # Example: get username from event data
    username = event['data']['object'].get('username')
    if not username:
        return {"error": "Missing username"}
    # ...rest of your logic (e.g., grant access)...
    return {"status": "ok"}
