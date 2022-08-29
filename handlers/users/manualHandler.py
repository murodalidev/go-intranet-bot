from aiogram import types

from loader import dp


@dp.message_handler(text="📜 Qo'llanma", state=None)
async def manual(msg: types.Message):
    await msg.reply("Bu bot orqali ro'yhatdan o'tsangiz sizga asakabanknig intranet tizimidan xabarlar jo'natilishi mumkin.")





