import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Get environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# Check if environment variables are set
if not api_id or not api_hash or not bot_token:
    raise ValueError("One or more environment variables are missing: API_ID, API_HASH, BOT_TOKEN")

# Convert API_ID to integer
try:
    api_id = int(api_id)
except ValueError:
    raise ValueError("API_ID must be an integer")

# Initialize Telegram Client
client = TelegramClient(StringSession(), api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("Bot is running! Use `/login` to log in to Udemy.")

client.run_until_disconnected()
