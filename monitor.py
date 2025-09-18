import os
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

# канали для моніторингу
CHANNELS = [
    -1001881412965,
    -1001246340723,
    -1001925047673,
    -1001795965474,
    -1001585782020,
    -1001661270840,
    -1002076377551,
    -1001943941408,
    -1001648319955,
    -1001495328651,
    -1001550392151,
    -1001744681450,
    -1001592219203,
    -1002158241088,
    -1001883710438,
    -1001615697742,
    -1001172446062,
    -1001605292217
]

# ключові слова
KEYWORDS = [
    "вантаж", "перевезти", "перевезення", "бус", "грузовий",
    "відвезти", "речі", "меблі", "вещи", "перевести", "грузовой"
]


@user.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    text = (event.message.message or "").lower()

    if any(k in text for k in KEYWORDS):
        chat = await event.get_chat()
        title = getattr(chat, "title", None) or getattr(chat, "username", None) or f"ID {chat.id}"

        # автор повідомлення
        sender = await event.get_sender()
        author = f"@{sender.username}" if sender and sender.username else "невідомий"

        # посилання на повідомлення
        if chat.username:
            link = f"https://t.me/{chat.username}/{event.id}"
        else:
            link = f"https://t.me/c/{str(chat.id)[4:]}/{event.id}"

        # формуємо повідомлення
        msg = (
            f"📢 <b>Чат:</b> {title}\n"
            f"📦 <b>Категорія:</b> Вантажні перевезення по країні\n"
            f"🌍 <b>Країна:</b> Бельгія\n"
            f"📍 <b>Регіон:</b> невідомо\n"
            f"🏙 <b>Місто:</b> невідомо\n"
            f"🔗 <b>Посилання на повідомлення:</b> {link}\n"
            f"👤 <b>Автор:</b> {author}\n\n"
            f"📝 <b>Текст:</b>\n{text}"
        )

        # 1. відправляємо оформлене повідомлення через бота
        await bot.send_message(MY_ID, msg, parse_mode="html")

        # 2. пересилаємо оригінал повідомлення через юзер-клієнта
        await user.forward_messages(MY_ID, event.message)


async def main():
    await bot.start(bot_token=BOT_TOKEN)
    await user.start()
    print("✅ Бот і юзер запущені")
    await user.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
