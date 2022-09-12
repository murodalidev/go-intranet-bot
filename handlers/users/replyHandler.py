from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from keyboards.default.homeKeyboard import homeKey
from states.personalData import ReplyMessage


@dp.callback_query_handler(text='reply')
@dp.message_handler(state=ReplyMessage.message_id)
async def reply_to_assignment(call: types.CallbackQuery, state: FSMContext):
    callback_data = call.data
    message_id = call.message.message_id
    await state.update_data(
        {'message_id': message_id}
    )

    await call.message.reply('Javobingizni yozing: ', reply_markup=homeKey)
    await call.answer(cache_time=1)
    await ReplyMessage.description.set()


@dp.message_handler(state=ReplyMessage.description)
async def write_description(msg: types.Message, state: FSMContext):
    description = msg.text
    await state.update_data(
        {"description": description}
    )
    state_data = await state.get_data()
    message_id = state_data.get('message_id')

    message = await db.select_message(message_id=message_id)

    await db.reply_to_assignment(
        sender_id=message[4],
        receiver_id=message[5],
        document_id=message[6],
        description=state_data.get('description'),
        success=True,
        message_id=message_id,
        created_date=datetime.now(),
    )
    await state.finish()
    await msg.answer("Xabaringiz qabul qilindi", reply_markup=homeKey)





