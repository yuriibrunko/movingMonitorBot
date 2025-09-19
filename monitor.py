import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Завантажуємо змінні оточення
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_ID = int(os.getenv("MY_ID"))
USER_SESSION_STRING = os.getenv("USER_SESSION_STRING")

# Юзер та бот клієнти
user = TelegramClient(StringSession(USER_SESSION_STRING), API_ID, API_HASH)
bot = TelegramClient("bot_session", API_ID, API_HASH)

# Канали для моніторингу
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

# Ключові слова
KEYWORDS = [
    # вантаж / груз
    "вантаж", "груз", "грузовой", "грузовий", "грузчик", "грузчики",

    # перевезення речей
    "перевезти", "перевезення", "перевести", "перевозка", "перевозчик", "перевізник",
    "перевезеня", "перевесення", "перевозка вещей", "перевозка мебелі",

    # переїзд
    "переїзд", "переезд", "переїз", "переізд", "relocation", "relokacia", "relokatsiya",

    # транспорт
    "бус", "бусик", "бусік", "мікроавтобус", "микроавтобус", "газель", "машина", "авто",
    "транспорт", "траспорт", "транспрт", "транспот", "транспарт", "траснпорт",

    # доставка
    "доставка", "доставити", "доставить", "вивіз", "вывоз",

    # речі
    "речі", "вещи", "посилка", "пакунок", "пакет", "коробка", "ящик",

    # меблі / техніка
    "меблі", "мебель", "диван", "шафа", "шкаф", "ліжко", "кровать",
    "стіл", "стол", "стільці", "стул", "техніка", "техника", "телевізор", "холодильник", "пральна машина",

    # 🚕 пасажирські перевезення
    "аеропорт", "аеропорту", "аеропорта", "airport", "charleroi", "шарлеруа", "brussels airport", "завентем",
    "поїздка", "поездка", "поиздка", "їхати", "поехать", "відвезти", "отвезти",
    "забрати", "заберете", "забрать", "зобрати", "заберати", "pick up", "drop off",
    "підкинути", "підвезти", "підвести", "ride",
    "таксі", "такси", "taxi", "uber", "bolt", "пасажир", "пасажири"
]

# Стоп-слова (ознаки реклами/комерції)
STOPWORDS = [
    "ціна", "ціни", "доступні", "швидко", "якісно", "надійно", "послуги", "гарантія",
    "телефонуйте", "звертайтесь", "надаю", "пропонуємо", "пропоную", "курси", "курс", "навчання", "інструктор", "школа", "тренінг", "навчатися",
    "viber", "вайбер", "whatsapp", "ватсап", "telegram", "tg:", "тел:", "📞", "📱", "+32", "+380"
]

# 📌 ID каналу/групи, куди складати переслані оригінали
TARGET_CHAT_ID = -1002932377188


@user.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    try:
        text = (event.message.message or "").lower()

        # 1. Перевіряємо ключові слова
        if not any(k in text for k in KEYWORDS):
            return

        # 2. Фільтруємо рекламу (стоп-слова)
        if any(s in text for s in STOPWORDS):
            return

        # Інфо про чат/канал
        chat = await event.get_chat()
        title = getattr(chat, "title", None) or getattr(chat, "username", None) or f"ID {chat.id}"

        # Автор
        sender = await event.get_sender()
        author = f"@{sender.username}" if sender and sender.username else "невідомий"

        # Лінк
        if getattr(chat, "username", None):
            link = f"https://t.me/{chat.username}/{event.id}"
        else:
            link = f"https://t.me/c/{str(chat.id)[4:]}/{event.id}"

        # Оформлене повідомлення
        msg = (
            f"📢 <b>Чат:</b> {title}\n"
            f"📦 <b>Категорія:</b> Перевезення (вантажні / пасажирські)\n"
            f"🌍 <b>Країна:</b> Бельгія\n"
            f"📍 <b>Регіон:</b> невідомо\n"
            f"🏙 <b>Місто:</b> невідомо\n"
            f"🔗 <b>Посилання на повідомлення:</b> {link}\n"
            f"👤 <b>Автор:</b> {author}\n\n"
            f"📝 <b>Текст:</b>\n{text}"
        )

        # 1) Надсилаємо оформлене повідомлення ботом
        await bot.send_message(MY_ID, msg, parse_mode="html")

        # 2) Пересилаємо оригінал у спеціальний канал
        await user.forward_messages(TARGET_CHAT_ID, event.message)

    except Exception as e:
        print("ERROR in handler:", repr(e))


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

