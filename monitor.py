import os
import time
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# завантажуємо змінні оточення
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_ID = int(os.getenv("MY_ID"))
USER_SESSION_STRING = os.getenv("USER_SESSION_STRING")

# створюємо клієнтів
user = TelegramClient(StringSession(USER_SESSION_STRING), API_ID, API_HASH)
bot = TelegramClient("bot_session", API_ID, API_HASH)

# канали, які реально моніторимо (⚠️ НЕ додавай сюди свого бота!)
CHANNELS = [
    "@o_brunko",
]

# ключові слова
KEYWORDS = [
    "вантаж", "перевезти", "перевезення", "бус", "грузовий",
    "відвезти", "речі", "меблі", "вещи", "перевести", "грузовой"
]

# антиспам (зберігаємо час останнього алерта для кожного каналу)
last_alert = {}


@user.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    text = (event.message.message or "").lower()

    if any(k in text for k in KEYWORDS):
        chat = await event.get_chat()
        title = getattr(chat, "title", None) or getattr(chat, "username", None) or f"ID {chat.id}"

        # антиспам: не більше 1 повідомлення з каналу за 60 секунд
        now = time.time()
        if chat.id in last_alert and now - last_alert[chat.id] < 60:
            return
        last_alert[chat.id] = now

        await bot.send_message(
            MY_ID,
            f"🔔 Знайшов збіг у <b>{title}</b>:\n\n{text}",
            parse_mode="html"
        )


async def main():
    # запускаємо обох клієнтів
    await bot.start(bot_token=BOT_TOKEN)
    await user.start()
    print("✅ Бот і юзер запущені")
    await user.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
