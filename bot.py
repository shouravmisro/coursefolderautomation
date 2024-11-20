from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

# Telegram API credentials
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# Initialize Telegram Client
client = TelegramClient(StringSession(), api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("Bot is running! Use `/login` to log in to Udemy.")

@client.on(events.NewMessage(pattern="/login"))
async def login(event):
    await event.reply("Send your Udemy email, password, and OTP one by one.\nUse:\n1. `/email your_email`\n2. `/password your_password`\n3. `/otp your_otp`")

# Command to test the bot's connection to the Telegram channel
@client.on(events.NewMessage(pattern="/test"))
async def test_channel(event):
    await event.reply("Testing connection to Telegram channel...")

client.run_until_disconnected()
