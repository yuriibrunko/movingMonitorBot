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

# ключові слова для пошуку
KEYWORDS = [
    # вантаж / груз
    "вантаж", "груз", "грузовой", "грузовий", "грузчик", "грузчики",

    # перевезення
    "перевезти", "перевезення", "перевести", "перевозка", "перевозчик", "перевізник",
    "перевезеня", "перевесення", "перевозка вещей", "перевозка мебелі",

    # переїзд
    "переїзд", "переезд", "переїз", "переізд", "relocation", "relokacia", "relokatsiya",

    # транспорт
    "бус", "бусик", "бусік", "бусикі", "бусикы",
    "мікроавтобус", "микроавтобус", "мікраавтобус",
    "газель", "газел", "gazel",
    "машина", "авто", "транспорт", "траспорт", "транспрт", "транспот", "транспарт", "траснпорт",

    # доставка
    "доставка", "доставити", "доставить", "достава", "доствка", "достака", "доставкa",
    "вивіз", "вывоз", "вивос",

    # речі
    "речі", "вещи", "реі", "веши", "вешчи",
    "посилка", "посылка", "пакунок", "пакет", "коробка", "коробки", "ящик",

    # меблі / техніка
    "меблі", "мебель", "мебел", "мєблі",
    "диван", "деван", "diwan",
    "шафа", "шофа", "шкаф",
    "ліжко", "ліжка", "ліжкко", "лижко", "кровать",
    "стіл", "стол", "stol", "стілл",
    "стільці", "стул", "стулья", "стілець",
    "техніка", "техника", "побутова техніка", "бытовая техника",
    "телевізор", "холодильник", "пральна машина", "стиралка"
]

# слова/патерни для реклами (їх треба відсіяти)
AD_KEYWORDS = [
    "надаю послуги", "пропоную перевезення", "послуги перевезення",
    "доставка по", "ціна", "прайс", "оплата", "24/7",
    "viber", "whatsapp", "telegram", "директ",
    "телефон", "дзвоніть", "звертайтесь",
    "+32", "+380", "+48", "+420", "097", "098", "050", "063", "073", "093",
    "🚚", "📦", "💶", "➡️", "✅", "✔️", "📞", "📱"
]

# ID каналу/групи для збереження оригіналів
TARGET_CHAT_ID = -1002932377188


@user.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    try:
        text = (event.message.message or "").lower()

        # 1. перевірка на ключові слова
        if not any(k in text for k in KEYWORDS):
            return

        # 2. відсіювання реклами
        if any(ad in text for ad in AD_KEYWORDS):
            print("⏩ Відсіяно рекламу:", text[:60])
            return

        # 3. отримуємо інформацію про чат
        chat = await event.get_chat()
        title = getattr(chat, "title", None) or getattr(chat, "username", None) or f"ID {chat.id}"

        # 4. автор повідомлення
        sender = await event.get_sender()
        author = f"@{sender.username}" if sender and sender.username else "невідомий"

        # 5. посилання на повідомлення
        if getattr(chat, "username", None):
            link = f"https://t.me/{chat.username}/{event.id}"
        else:
            link = f"https://t.me/c/{str(chat.id)[4:]}/{event.id}"

        # 6. формуємо красиво оформлене повідомлення
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

        # 7. надсилаємо повідомлення тобі
        try:
            await bot.send_message(MY_ID, msg, parse_mode="html")
        except Exception as e:
            print("ERROR: bot.send_message failed:", repr(e))

        # 8. пересилаємо оригінал у канал
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

