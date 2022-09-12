from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loader import dp


# Home
@dp.message_handler(text='🔙 Orqaga qaytish', state='*')
async def home(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Asosiy menuga qaytdingiz \nbotni qayta ishlatish uchun /start kmandasini ustiga bosing!", reply_markup=ReplyKeyboardRemove())