# bots/discord_bot.py
import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
if not TOKEN or not CHANNEL_ID:
    raise EnvironmentError("Missing DISCORD_BOT_TOKEN or DISCORD_CHANNEL_ID in environment variables.")
CHANNEL_ID = int(CHANNEL_ID)

class WhaleClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        channel = self.get_channel(CHANNEL_ID)
        await channel.send("TradingWhale bot online!")

    async def post_signal(self, message, image_path=None):
        channel = self.get_channel(CHANNEL_ID)
        if image_path:
            with open(image_path, 'rb') as f:
                await channel.send(content=message, file=discord.File(f))
        else:
            await channel.send(message)

client = WhaleClient(intents=discord.Intents.default())
client.run(TOKEN)