import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from bot import *


async def main():
    load_dotenv()

    bot = Bot(os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(weather_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(menu_commands)
    await dp.start_polling(bot)



asyncio.run(main())
