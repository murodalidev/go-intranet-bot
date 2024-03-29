import json
import os
from datetime import datetime

import requests
import websockets
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.homeKeyboard import homeKey
from loader import dp, db, bot
from states.personalData import ReplyMessage


@dp.callback_query_handler(text='reply')
@dp.message_handler(state=ReplyMessage.message_id)
async def reply_to_assignment(call: types.CallbackQuery, state: FSMContext):
    message_id = call.message.message_id
    await state.update_data(
        {'message_id': message_id}
    )
    await call.message.reply('Javobingizni yozing: ', reply_markup=homeKey)
    await call.answer(cache_time=1)
    await ReplyMessage.description.set()


def get_token():
    data = {
        "username": os.getenv("INTRANET_BOT_USERNAME"),
        "password": os.getenv("INTRANET_BOT_PASSWORD")
    }
    res = requests.post('https://intranet-api.asakabank.uz/login/', json=data, verify=False).json()

    return res.get('access')


async def send_message_via_socket(chat_id, new_msg):
    url = f'wss://intranet-api.asakabank.uz/ws/?token={get_token()}'
    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps({'command': 'user_handshake'}))
        await websocket.recv()
        await websocket.send(json.dumps({'command': 'chat_handshake', 'chat_id': chat_id, 'chat_type': 'bot'}))
        await websocket.recv()
        await websocket.send(json.dumps(new_msg))
        await websocket.recv()


CONTENT_TYPES = ["text", "document", "photo", "video", "video_note", "contact"]


@dp.message_handler(state=ReplyMessage.description, content_types=CONTENT_TYPES)
async def write_description(msg: types.Message, state: FSMContext):
    description = msg.text
    await state.update_data(
        {"description": description}
    )
    state_data = await state.get_data()
    message_id = state_data.get('message_id')
    message = await db.select_message(message_id=message_id)
    chat_id = message[8]
    document_id = None

    data = await db.select_user(id=message[4])
    tg_user = [
        data[0]
    ]
    new_msg = {
        'command': 'new_message',
        'chat_id': chat_id,
        'chat_type': 'bot',
        'text': state_data.get('description'),
        'message_type': 'BOT_MESSAGE',
        'telegram_users': tg_user
    }
    # await db.save_reply_to_intranet_chatbot(
    #     sender_id=9749,
    #     created_by_id=9749,
    #     modified_by_id=9749,
    #     type='BOT_MESSAGE',
    #     chat_id=chat_id,
    #     file_id=None,
    #     telegram_users=json.dumps(tg_user),
    #     created_date=datetime.now(),
    #     modified_date=datetime.now(),
    #     text=state_data.get('description'),
    #     edited=False,
    #     deleted=False
    # )
    if msg.content_type == "text":
        await send_message_via_socket(chat_id, new_msg)
        await state.finish()
        await msg.answer("Xabaringiz qabul qilindi", reply_markup=homeKey)

    if msg.content_type == "photo":
        await msg.answer("Iltimos fayl formatida jo'nating!", reply_markup=homeKey)

    if msg.content_type == "document":
        file_id_doc = msg.document.file_id
        file_obj = await bot.get_file(file_id_doc)
        file_path = file_obj.file_path
        file = await bot.download_file(file_path)

        upload_url = "https://intranet-api.asakabank.uz/upload/"
        upload_payload = {}
        upload_payload_files = {
            ('document', (f'{file_path.split("/")[-1]}', file, '*'))
        }
        upload_file = requests.post(url=upload_url, data=upload_payload, files=upload_payload_files, verify=False)
        document_id = upload_file.json().get('id')
        ext = msg.document.mime_type.split('/')[-1]
        new_msg['file'] = document_id
        new_msg['text'] = msg.caption
        new_msg['ext'] = ext
        await send_message_via_socket(chat_id, new_msg)
        await state.finish()
        await msg.answer("Xabaringiz qabul qilindi", reply_markup=homeKey)

    await db.reply_to_assignment(
        sender_id=message[4],
        receiver_id=message[5],
        document_id=document_id,
        chat_id=chat_id,
        description=state_data.get('description'),
        success=True,
        message_id=message_id,
        created_date=datetime.now()
    )
