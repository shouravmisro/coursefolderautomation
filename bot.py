import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Get environment variables
api_id = 21724120
api_hash = '4936c90454e2951d281eb0176c193875'
bot_token = '7588623586:AAH8TQ2j3ehncRKnfnQZkqsu8Zdh0Hx4cSg'

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

@client.on(events.NewMessage(pattern="/login"))
async def login(event):
    await event.reply("Send your Udemy email, password, and OTP one by one.\nUse:\n1. `/email your_email`\n2. `/password your_password`\n3. `/otp your_otp`")

# Command to test the bot's connection to the Telegram channel
@client.on(events.NewMessage(pattern="/test"))
async def test_channel(event):
    await event.reply("Testing connection to Telegram channel...")

client.run_until_disconnected()
