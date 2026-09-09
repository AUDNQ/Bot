import asyncio
from aiogram import Dispatcher
from loader import bot 
from tghandlers import router

async def main():
    dp = Dispatcher()
    dp.include_router(router)

    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())