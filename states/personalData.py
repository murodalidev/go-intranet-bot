from aiogram.dispatcher.filters.state import State, StatesGroup


class PersonalData(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    confirm = State()


class ReplyMessage(StatesGroup):
    message_id = State()
    description = State()

