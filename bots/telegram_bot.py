from telegram import Bot
import os, logging

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
if not TELEGRAM_TOKEN or not TELEGRAM_CHANNEL_ID:
    raise EnvironmentError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID in environment variables.")
bot = Bot(token=TELEGRAM_TOKEN)

def send_signal_message(text, image_path):
    try:
        with open(image_path, 'rb') as img:
            bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID, photo=img, caption=text)
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {e}")
