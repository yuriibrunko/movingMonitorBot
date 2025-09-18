# import os
# import time
# import asyncio
# from dotenv import load_dotenv
# from telethon import TelegramClient, events
# from telethon.sessions import StringSession

# # завантажуємо змінні оточення
# load_dotenv()
# API_ID = int(os.getenv("API_ID"))
# API_HASH = os.getenv("API_HASH")
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# MY_ID = int(os.getenv("MY_ID"))
# USER_SESSION_STRING = os.getenv("USER_SESSION_STRING")

# # створюємо клієнтів
# user = TelegramClient(StringSession(USER_SESSION_STRING), API_ID, API_HASH)
# bot = TelegramClient("bot_session", API_ID, API_HASH)

# # канали для моніторингу
# CHANNELS = [
#     "@o_brunko",
#     "-1001495328651",
#     "@ukraine_anwerp",
#     "@BelgiaN1",
#     "@belgia_ukr",
#     "@belgia_ukraina",
#     "@ours_in_belgium",
#     "@belgiumua1",
#     "@refugeesinBelgium",
#     "@NL_BL_transport_work",
#     "@ukrainians_in_the_NL",
#     "@ukrayintsi_v_belhiyi",
#     "@NL_BL_transport_work"
# ]

# # ключові слова
# KEYWORDS = [
#     "вантаж", "перевезти", "перевезення", "бус", "грузовий",
#     "відвезти", "речі", "меблі", "вещи", "перевести", "грузовой"
# ]

# # антиспам
# last_alert = {}


# @user.on(events.NewMessage(chats=CHANNELS))
# async def handler(event):
#     text = (event.message.message or "").lower()

#     if any(k in text for k in KEYWORDS):
#         chat = await event.get_chat()
#         title = getattr(chat, "title", None) or getattr(chat, "username", None) or f"ID {chat.id}"

#         # автор повідомлення
#         sender = await event.get_sender()
#         author = f"@{sender.username}" if sender and sender.username else "невідомий"

#         # посилання на повідомлення (тільки якщо канал має username)
#         if chat.username:
#             link = f"https://t.me/{chat.username}/{event.id}"
#         else:
#             # для приватних/ID каналів (формат /c/...)
#             link = f"https://t.me/c/{str(chat.id)[4:]}/{event.id}"

#         # антиспам: не більше 1 повідомлення з каналу за 60 секунд
#         now = time.time()
#         if chat.id in last_alert and now - last_alert[chat.id] < 60:
#             return
#         last_alert[chat.id] = now

#         # формуємо повідомлення
#         msg = (
#             f"📢 <b>Чат:</b> {title}\n"
#             f"📦 <b>Категорія:</b> Вантажні перевезення по країні\n"
#             f"🌍 <b>Країна:</b> Бельгія\n"
#             f"📍 <b>Регіон:</b> невідомо\n"
#             f"🏙 <b>Місто:</b> невідомо\n"
#             f"🔗 <b>Посилання на повідомлення:</b> {link}\n"
#             f"👤 <b>Автор:</b> {author}\n\n"
#             f"📝 <b>Текст:</b>\n{text}"
#         )

#         await bot.send_message(MY_ID, msg, parse_mode="html")


# async def main():
#     await bot.start(bot_token=BOT_TOKEN)
#     await user.start()
#     print("✅ Бот і юзер запущені")
#     await user.run_until_disconnected()

from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH"))
USER_SESSION_STRING = os.getenv("USER_SESSION_STRING")

with TelegramClient(StringSession(USER_SESSION_STRING), API_ID, API_HASH) as client:
    dialogs = client.get_dialogs()
    for dialog in dialogs:
        if dialog.is_channel:
            print(f"Назва: {dialog.name} | ID: {dialog.id}")


# if __name__ == "__main__":
#     asyncio.run(main())
