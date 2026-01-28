from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

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
            await message.answer("Siz avval ro'yxatdan o'tgansiz!")
            return
        
    phone_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Send Phone", request_contact=True)]
            ],
        resize_keyboard=True
    )
    text = f"""
    Salom {message.from_user.first_name} 👋  
FastAPI loyihamizning rasmiy botiga xush kelibsiz 🚀  

⬇️ Tasdiqlash kodini olish uchun  
telefon raqamingizni yuboring  
(tugmani bosish orqali)
"""
    await message.answer(text=text, reply_markup=phone_keyboard)
  
  
@dp.message(F.contact)  
async def handle_contact(message:Message):
    chat_id = message.from_user.id
    phone_number = message.contact.phone_number
    if not phone_number.startswith("+"):
        phone_number ="+" + phone_number
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name if message.from_user.last_name is not None else f"username_{chat_id}"
    username = message.from_user.username if message.from_user.username  is not None else f"username_{chat_id}"
    url = f"{settings.HOST}/api/v1/users/register"
    body = {
        "first_name":first_name,
        "last_name":last_name,
        "username":username,
        "phone_number":phone_number,
        "chat_id":str(chat_id)
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, json=body)
        if response.status_code == status.HTTP_200_OK:
            code = response.json().get("code") 
            await message.answer(text=f"Ro'yxatdan muvaffaqiyatli o'tildi. Sizning kodingiz {code}")

async def main():
    await dp.start_polling(bot)
    logging.info("Bot ishga tushdi!")
    
    
if __name__ == "__main__":
    asyncio.run(main())
    