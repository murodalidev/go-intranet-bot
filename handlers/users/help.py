from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: types.Message, state: FSMContext):
    await state.finish()
    text = ("Buyruqlar: ",
            "/start - Botni qayta ishga tushurish",
            )
    
    await message.answer("\n".join(text))
