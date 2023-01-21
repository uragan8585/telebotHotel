import calendar
import handlers.default_heandlers.start

from loader import bot
from telebot import types
from telebot.types import Message
from states.contact_information import UserInfoState
from api_requests import get_meta_data
from keyboards.reply import list_button
from keyboards.inline import calendar
from datetime import datetime



def get_hotel(message: Message):
    data = bot.current_states
    curr_city = get_meta_data.list_cities(user_country=data['city'])
    print(curr_city)
    try:
        lst_hotels = get_meta_data.list_hotels(user_city=curr_city[0][1],
                                               qty_hotels=data['qty_hotels'],
                                               checkIn=data['data_check_in'],
                                               checkOut=data['data_check_out'])

        for hotels in lst_hotels:
            bot.send_message(message.from_user.id, f'Название отеля: {hotels[0]}'
                                                   f'\nЦена за сутки: {hotels[2]}')
            if data['need_photo'] == 'Да':
                lst_photo = get_meta_data.list_photo(value=hotels[1])
                for photo in lst_photo:
                    bot.send_photo(message.from_user.id, photo)
        bot.send_message(message.from_user.id, f'Главное меню /start')

    except Exception as err:
        bot.send_message(message.from_user.id, 'Поиск не удался. Попробуйте ещё раз.'
                                               '\n/start')
        bot.delete_state(message.from_user.id, message.chat.id)
