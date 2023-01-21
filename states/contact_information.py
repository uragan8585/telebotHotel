from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    user_id = State()
    name = State()
    country = State()
    city = State()
    qty_hotels = State()
    need_photo = State()
    qty_photo = State()
    phone_number = State()
    data_check_in = State()
    data_check_out = State()
