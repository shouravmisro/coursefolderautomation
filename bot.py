import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# Get environment variables
api_id = 21724120
api_hash = '4936c90454e2951d281eb0176c193875'
bot_token = '7588623586:AAH8TQ2j3ehncRKnfnQZkqsu8Zdh0Hx4cSg'

client = TelegramClient(StringSession(), api_id, api_hash).start(bot_token=bot_token)

# Temporary storage for user login info
user_login_info = {}

# Start command
@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("Bot is running! Use `/login` to log in to Udemy or `/enroll` to enroll in courses.")

# Login command
@client.on(events.NewMessage(pattern="/login"))
async def login(event):
    chat_id = event.sender_id
    user_login_info[chat_id] = {}

    await event.reply("Please enter your Udemy email:")
    user_login_info[chat_id]['step'] = 'email'

# Handle the email, password, and OTP input
@client.on(events.NewMessage)
async def handle_login(event):
    chat_id = event.sender_id

    # Check if the user is in the login flow
    if chat_id in user_login_info and 'step' in user_login_info[chat_id]:
        step = user_login_info[chat_id]['step']
        
        # Handle email input
        if step == 'email':
            user_login_info[chat_id]['email'] = event.text
            user_login_info[chat_id]['step'] = 'password'
            await event.reply("Email saved! Now enter your Udemy password:")

        # Handle password input
        elif step == 'password':
            user_login_info[chat_id]['password'] = event.text
            user_login_info[chat_id]['step'] = 'otp'
            await event.reply("Password saved! If OTP is required, please enter it. Otherwise, type 'skip':")

        # Handle OTP input
        elif step == 'otp':
            user_login_info[chat_id]['otp'] = event.text if event.text.lower() != 'skip' else None
            await event.reply("All login info received. Attempting to log in...")
            
            # Call a function to log in to Udemy
            result = udemy_login(user_login_info[chat_id])
            if result:
                await event.reply("Successfully logged in to Udemy!")
            else:
                await event.reply("Failed to log in. Please check your credentials and try again.")
            
            # Clear user info after login attempt
            user_login_info.pop(chat_id, None)

# Mock Udemy login function (to be replaced with actual implementation)
def udemy_login(login_info):
    email = login_info['email']
    password = login_info['password']
    otp = login_info['otp']
    # Mock login logic: Replace this with real automation for logging in
    print(f"Logging in with Email: {email}, Password: {password}, OTP: {otp}")
    time.sleep(2)  # Simulating login delay
    return True  # Assume success for now
enrolled_courses = []

@client.on(events.NewMessage(pattern="/enroll"))
async def enroll(event):
    chat_id = event.sender_id

    await event.reply("Send me the Udemy course link to enroll.")
    
    @client.on(events.NewMessage)
    async def handle_enroll(event):
        course_link = event.text
        
        # Automate enrollment using Selenium
        result = enroll_course(course_link)
        
        if result:
            enrolled_courses.append(course_link)
            await event.reply(f"Successfully enrolled in the course: {course_link}")
            
            # Save enrollment to Excel
            save_to_excel(enrolled_courses)
        else:
            await event.reply("Failed to enroll in the course. Please try again.")

# Function to automate course enrollment
def enroll_course(course_link):
    try:
        # Set up the Chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Navigate to the course link and enroll
        driver.get(course_link)
        enroll_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Enroll')]")
        enroll_button.click()
        time.sleep(2)  # Simulating enrollment delay
        
        driver.quit()
        return True
    except Exception as e:
        print(f"Error enrolling in course: {e}")
        return False

# Function to save enrollment data to Excel
def save_to_excel(courses):
    df = pd.DataFrame(courses, columns=["Enrolled Courses"])
    df.to_excel("enrolled_courses.xlsx", index=False)
# Run the bot
client.run_until_disconnected()
