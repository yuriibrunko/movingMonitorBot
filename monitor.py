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
bot = TelegramClient("bot_session", API_ID, API_HASH)

CHANNELS = ["@MovingMonitorBot"]  # тут краще список каналів, які реально хочеш моніторити
KEYWORDS = ["вантаж", "перевезти", "перевезення", "бус", "грузовий",
            "відвезти", "речі", "меблі", "вещи", "перевести", "грузовой"]

@user.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    text = (event.message.message or "").lower()
    if any(k in text for k in KEYWORDS):
        # Витягуємо назву каналу
        chat = await event.get_chat()
        title = getattr(chat, "title", None) or getattr(chat, "username", None) or f"ID {chat.id}"

        # Відправляємо тільки 1 повідомлення
        await bot.send_message(
            MY_ID,
            f"🔔 Знайшов збіг у <b>{title}</b>:\n\n{text}",
            parse_mode="html"
        )

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    await user.start()
    print("✅ Бот і юзер запущені")
    await user.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
