from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from typing import List
import os, requests, logging

app = FastAPI()

BREVO_API_KEY = os.getenv("BREVO_KEY")
BREVO_WEBHOOK_SECRET = os.getenv("BREVO_WEBHOOK_SECRET")
if not BREVO_API_KEY or not BREVO_WEBHOOK_SECRET:
    raise EnvironmentError("Missing BREVO_KEY or BREVO_WEBHOOK_SECRET in environment variables.")

class WebhookPayload(BaseModel):
    event: str
    email: str
    tags: List[str] = Field(default_factory=list)

@app.post("/webhook/brevo")
async def brevo_webhook(request: Request, payload: WebhookPayload):
    if request.headers.get("X-Webhook-Secret") != BREVO_WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")
    logging.info(f"Received Brevo event: {payload.event} for {payload.email}")
    if "lead_pdf" in payload.tags:
        logging.info(f"Lead downloaded PDF: {payload.email}")
        add_tag_to_contact(payload.email, "engaged_lead")
    return {"status": "ok"}

def add_tag_to_contact(email: str, tag: str):
    url = "https://api.brevo.com/v3/contacts"
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "updateEnabled": True,
        "tags": [tag]
    }
    try:
        resp = requests.put(url, json=data, headers=headers)
        if resp.status_code >= 400:
            logging.error(f"Failed tagging {email}: {resp.text}")
    except Exception as e:
        logging.error(f"Exception tagging {email}: {e}")
