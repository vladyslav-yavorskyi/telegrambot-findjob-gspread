from decouple import config
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.chat_action import ChatActionMiddleware

from google_spread import getClient
from handlers import router

TOKEN = config('TOKEN')


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.message.middleware(ChatActionMiddleware())
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())