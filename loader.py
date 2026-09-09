import os
from dotenv import load_dotenv
from aiogram import Bot
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ Не найден BOT_TOKEN в .env файле!")

bot = Bot(token=TOKEN)