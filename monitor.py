import os
import asyncio
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

KEYWORDS = [
    "вантаж", "перевезти", "перевезення", "бус", "грузовий", "привезти",
    "відвезти", "речі", "меблі", "ліжкко", "вещи", "перевести", "грузовой"
]

# 📌 ID каналу/групи, куди складати переслані оригінали
# заміни -1002223334445 на ID свого каналу (має починатись з -100...)
TARGET_CHAT_ID = -1002932377188


@user.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    try:
        text = (event.message.message or "").lower()

        if not any(k in text for k in KEYWORDS):
            return

        # отримуємо інформацію про чат/канал
        chat = await event.get_chat()
        title = getattr(chat, "title", None) or getattr(chat, "username", None) or f"ID {chat.id}"

        # автор повідомлення
        sender = await event.get_sender()
        author = f"@{sender.username}" if sender and sender.username else "невідомий"

        # лінк на повідомлення
        if getattr(chat, "username", None):
            link = f"https://t.me/{chat.username}/{event.id}"
        else:
            link = f"https://t.me/c/{str(chat.id)[4:]}/{event.id}"

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

        # 1) Відправляємо оформлене повідомлення ботом
        try:
            await bot.send_message(MY_ID, msg, parse_mode="html")
        except Exception as e:
            print("ERROR: bot.send_message failed:", repr(e))

        # 2) Пересилаємо оригінал у канал/групу для архіву
        try:
            await user.forward_messages(TARGET_CHAT_ID, event.message)
        except Exception as e:
            print("ERROR: forward_messages failed:", repr(e))

    except Exception as main_exc:
        print("ERROR in handler:", repr(main_exc))


async def main():
    await bot.start(bot_token=BOT_TOKEN)
    await user.start()
    print("✅ Бот і юзер запущені")
    await user.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())


# скрипт для виведення id телеграм каналів
# import os
# from dotenv import load_dotenv
# from telethon import TelegramClient
# from telethon.sessions import StringSession

# load_dotenv()
# API_ID = int(os.getenv("API_ID"))
# API_HASH = os.getenv("API_HASH")
# USER_SESSION_STRING = os.getenv("USER_SESSION_STRING")

# user = TelegramClient(StringSession(USER_SESSION_STRING), API_ID, API_HASH)

# async def main():
#     async for dialog in user.iter_dialogs():
#         if dialog.is_channel:  # тільки канали (ігноруємо чати/ботів/PM)
#             print(f"{dialog.name} → {dialog.id}")

# with user:
#     user.loop.run_until_complete(main())

