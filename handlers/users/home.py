from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from loader import dp


# Home
@dp.message_handler(text='🔙 Orqaga qaytish', state='*')
async def home(message: types.Message):
    await message.answer("Asosiy menuga qaytdingiz \nbotni qayta ishlatish uchun /start kmandasini ustiga bosing!", reply_markup=ReplyKeyboardRemove())