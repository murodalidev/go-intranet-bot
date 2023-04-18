import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.registerKeyboard import registerKey
from loader import dp, db


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    logging.info(message)
    await state.finish()
    user = await db.select_user(telegram_id=str(message.from_user.id)) or None
    if user is not None:
        await message.answer(f"Assalomu Alaykum, {user[3]} {user[4]}.\nSiz ro'yhatdan o'tib bo'lgansiz.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f"Assalomu Alaykum, {message.from_user.full_name}!", reply_markup=registerKey)




