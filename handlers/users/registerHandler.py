from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext

from keyboards.default.registerKeyboard import sendPhoneKey, confirmKey
from states.personalData import PersonalData

from datetime import datetime


@dp.message_handler(text="Ro'yhatdan o'tish", state=None)
async def start_ref(msg: types.Message):
    await msg.reply("Ro'yhatdan o'tish qismiga xush kelibsiz.\nIltimos kiritayortgan ma'lumotlaringizni tog'ri va to'liq shaklda kiriting.")
    await msg.answer("Ismingizni kiriting.", reply_markup=ReplyKeyboardRemove())
    await PersonalData.first_name.set()


@dp.message_handler(state=PersonalData.first_name)
async def write_first_name(msg: types.Message, state: FSMContext):
    first_name = msg.text
    await state.update_data(
        {"first_name": first_name}
    )
    await msg.answer('Familiyangizni kiriting.')
    await PersonalData.last_name.set()


@dp.message_handler(state=PersonalData.last_name)
async def write_last_name(msg: types.Message, state: FSMContext):
    last_name = msg.text
    await state.update_data(
        {"last_name": last_name}
    )
    await PersonalData.phone.set()
    await msg.answer("Raqamingizni jo'nating!", reply_markup=sendPhoneKey)


@dp.message_handler(content_types='contact', is_sender_contact=True, state=PersonalData.phone)
async def send_phone(msg: types.Message, state: FSMContext):
    phone = msg.contact.phone_number
    await state.update_data(
        {"phone": phone}
    )
    await PersonalData.confirm.set()

    state_data = await state.get_data()
    first_name = state_data.get('first_name')
    last_name = state_data.get('last_name')
    phone = state_data.get('phone')

    response = "Quyidagi malumotlar qabul qilindi:\n"
    response += f"Ismingiz: {first_name}\n"
    response += f"Familiyangiz: {last_name}\n"
    response += f"Raqamingiz: {phone}\n"

    await msg.answer("Kiritilgan ma'lumotlar to'gimi?", reply_markup=confirmKey)
    await msg.answer(response)


@dp.message_handler(state=PersonalData.confirm)
async def confirm(msg: types.Message, state: FSMContext):
    text = msg.text

    if text == "✅ Tasdiqlayman":
        state_data = await state.get_data()

        first_name = state_data.get('first_name')
        last_name = state_data.get('last_name')
        phone = state_data.get('phone')

        telegram_id =  msg.from_user.id
        username = msg.from_user.username or None
        created_date = datetime.now()

        await db.add_user(
            telegram_id=str(telegram_id),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            created_date=created_date,
        )
        await state.finish()
        await msg.answer('Muvofaqiyatli yakunlandi.', reply_markup=ReplyKeyboardRemove())
        for admin in ADMINS:
            await bot.send_message(chat_id=admin, text=f"telegram_id: {telegram_id}\nusername: {username}\nfull_name: {first_name} {last_name}\nphone: {phone}\ncreated_date: {created_date}")
    else:
        await state.finish()
        await msg.answer("Ismingizni kiriting.", reply_markup=ReplyKeyboardRemove())
        await PersonalData.first_name.set()

