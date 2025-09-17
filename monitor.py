import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_ID = int(os.getenv("MY_ID"))
USER_SESSION_STRING = os.getenv("USER_SESSION_STRING")

user = TelegramClient(StringSession(USER_SESSION_STRING), API_ID, API_HASH)
bot = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

CHANNELS = ["@MovingMonitorBot"]
KEYWORDS = ["вантаж", "перевезти", "перевезення", "бус", "грузовий", "відвезти", "перевезти", "речі", "меблі", "вещи", "перевести", "грузовой"]

@user.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    text = (event.message.message or "").lower()
    if any(k in text for k in KEYWORDS):
        title = getattr(event.chat, "title", "невідомий канал")
        await bot.send_message(MY_ID, f"🔔 Знайшов збіг у {title}:\n\n{text}")

if __name__ == "__main__":
    user.start()
    user.run_until_disconnected()
