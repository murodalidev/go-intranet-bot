import asyncio
import json
import os

import websockets
import requests
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


def get_token():
    data = {
        "username": os.getenv("INTRANET_BOT_USERNAME"),
        "password": os.getenv("INTRANET_BOT_PASSWORD")
    }
    res = requests.post('https://intranet-api.asakabank.uz/login/', json=data).json()

    return res.get('token')


async def connect_socket():
    url = f'wss://intranet-api.asakabank.uz/ws/?token={get_token()}'
    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps({'command': 'user_handshake'}))
        # await websocket.send(json.dumps({'command': 'chat_handshake', 'chat_id': 1092, 'chat_type': 'bot'}))
        await websocket.recv()


async def socket_chat_handshake(chat_id):
    url = f'wss://intranet-api.asakabank.uz/ws/?token={get_token()}'
    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps({'command': 'chat_handshake', 'chat_id': chat_id, 'chat_type': 'bot'}))
        await websocket.recv()


async def send_message_via_socket(data):
    url = f'wss://intranet-api.asakabank.uz/ws/?token={get_token()}'
    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps(data))
        await websocket.recv()


async def run_socket(chat_id, new_msg):
    asyncio.get_event_loop().run_until_complete(connect_socket())
    asyncio.get_event_loop().run_until_complete(socket_chat_handshake(chat_id))
    asyncio.get_event_loop().run_until_complete(send_message_via_socket(new_msg))


@dp.message_handler(state=ReplyMessage.description)
async def write_description(msg: types.Message, state: FSMContext):
    description = msg.text
    await state.update_data(
        {"description": description}
    )
    state_data = await state.get_data()
    message_id = state_data.get('message_id')

    message = await db.select_message(message_id=message_id)
    chat_id = message[8]

    await db.reply_to_assignment(
        sender_id=message[4],
        receiver_id=message[5],
        document_id=message[6],
        chat_id=chat_id,
        description=state_data.get('description'),
        success=True,
        message_id=message_id,
        created_date=datetime.now()
    )

    data = await db.select_user(id=message[4])
    tg_user = {
        'id': data[0],
        'username': data[2],
        'first_name': data[3],
        'last_name': data[4],
        'phone': data[5]
    }
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
    await state.finish()
    await msg.answer("Xabaringiz qabul qilindi", reply_markup=homeKey)
    await run_socket(chat_id=chat_id, new_msg=new_msg)
