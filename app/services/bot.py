from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from fastapi import status
from app.schemas import settings


import asyncio
import logging
import httpx


bot = Bot(token=settings.BOT_TOKEN)

dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message:Message):
    chat_id = message.from_user.id
    url = f"{settings.HOST}/check_user/{chat_id}"
    async with httpx.AsyncClient() as client:
        user = await client.get(url=url)
        if user.status_code == status.HTTP_200_OK:
            print("Bu royxatdan otgan")
        else:
            print("royxatdan otmagan")
    
    await message.answer(text="Salom!")
    
    
async def main():
    await dp.start_polling(bot)
    logging.info("Bot ishga tushdi!")
    
    
if __name__ == "__main__":
    asyncio.run(main())
    