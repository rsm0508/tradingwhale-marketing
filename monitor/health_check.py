# monitor/health_check.py
import subprocess
import os
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
if not TELEGRAM_TOKEN or not TELEGRAM_CHANNEL_ID:
    raise EnvironmentError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID in environment variables.")
bot = Bot(token=TELEGRAM_TOKEN)

HEALTH_CHECKS = [
    ("n8n", "docker inspect -f '{{.State.Health.Status}}' tradingwhale_n8n_1"),
    ("screenshot_service", "docker inspect -f '{{.State.Health.Status}}' tradingwhale_screenshot_1"),
]

def check_services():
    for name, cmd in HEALTH_CHECKS:
        try:
            result = subprocess.check_output(cmd, shell=True).decode().strip()
            if result != "healthy":
                bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=f"Service {name} is unhealthy: {result}")
        except Exception as e:
            bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=f"Health check error on {name}: {str(e)}")

if __name__ == "__main__":
    check_services()
