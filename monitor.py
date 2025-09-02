import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

# Завантажуємо змінні з .env
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
my_id = int(os.getenv("MY_ID"))

# Створюємо клієнти
user = TelegramClient("user_session", api_id, api_hash)
bot = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

# Ключові слова (під твою тему)
KEYWORDS = [
    "вантаж", "вантажі", "вантажне", "вантажоперевезення", "перевезення",
    "доставка", "перевізник", "логістика", "фура", "єврофура", "тент",
    "реф", "рефрижератор", "ТТН", "CMR", "FTL", "LTL",
    "груз", "грузы", "грузоперевозки", "перевозка", "перевозчик",
    "freight", "cargo", "shipping", "truck", "logistics", "reefer"
]

# Канали для моніторингу
CHANNELS = ["@назва_каналу1", "@назва_каналу2"]

@user.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    text = event.message.message.lower()
    if any(keyword in text for keyword in KEYWORDS):
        await bot.send_message(
            my_id,
            f"🔔 Знайшов збіг у {event.chat.title}:\n\n{text}"
        )

# Запускаємо
user.start()
user.run_until_disconnected()
