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
from utils import get_hotels


@bot.message_handler(commands=['low'])
def start_survey(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.country, message.chat.id)
    bot.send_message(message.from_user.id, f'Введите страну (на английском языке)\nТак же можете выбрать из списка')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_id'] = message.from_user.id

    lst_country = get_meta_data.list_country()
    list_button.list_button(message, lst_country)


@bot.message_handler(state=UserInfoState.country)
def get_country(message: Message) -> None:
    country = message.text.replace(' ', '')
    if country.isalpha():
        bot.send_message(message.from_user.id, 'Отличный выбор. Записал. Введите город (на английском языке)\n'
                                               'Так же можете выбрать из списка')
        bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['country'] = message.text.upper()

        lst_cities = get_meta_data.list_cities(user_country=data['country'])
        list_button.list_button(message=message, lts=lst_cities)
    else:
        bot.send_message(message.from_user.id, 'Название страны может содержать только буквы')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['country'] = ''


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    city = message.text.replace(' ', '')
    if city.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо, записал. Напишите дату заселения "ГГГГ-ММ-ДД"')
        bot.set_state(message.from_user.id, UserInfoState.data_check_in, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Название города может содержать только буквы')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = ''


@bot.message_handler(state=UserInfoState.data_check_in)
def get_data_check_in(message: Message) -> None:
    try:
        datetime.strptime(message.text, '%Y-%m-%d')
        bot.send_message(message.from_user.id, 'Спасибо, записал. Укажите дату выезда')
        bot.set_state(message.from_user.id, UserInfoState.data_check_out, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['data_check_in'] = message.text

    except ValueError as err:
        bot.send_message(message.from_user.id, 'Напишите дату заселения "ГГГГ-ММ-ДД"')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['data_check_in'] = ''


@bot.message_handler(state=UserInfoState.data_check_out)
def data_check_out(message: Message) -> None:
    try:
        datetime.strptime(message.text, '%Y-%m-%d')
        bot.send_message(message.from_user.id, 'Спасибо, записал. Количество отелей, которые необходимо вывести'
                                               '(не более 10)')
        bot.set_state(message.from_user.id, UserInfoState.qty_hotels, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['data_check_out'] = message.text

    except ValueError:
        bot.send_message(message.from_user.id, 'Напишите дату выезда "ГГГГ-ММ-ДД"')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['data_check_out'] = ''


@bot.message_handler(state=UserInfoState.qty_hotels)
def get_qty_hotels(message: Message) -> None:
    if message.text.isdigit() and int(message.text) in range(1, 11):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        markup.add('Да', 'Нет')
        bot.send_message(message.from_user.id, 'Спасибо, записал. Показать фотографий для каждого отеля?',
                         reply_markup=markup)
        bot.set_state(message.from_user.id, UserInfoState.need_photo, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['qty_hotels'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Введите цифрами количество отелей и не более 10')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['qty_hotels'] = ''


@bot.message_handler(state=UserInfoState.need_photo)
def get_need_photo(message: Message) -> None:
    if (message.text == u'Да') or (message.text == u'Нет'):
        # if message.text == u'Нет':
            bot.send_message(message.from_user.id, 'Спасибо, записал. Выбираю лучшие предложения')

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['need_photo'] = message.text
        # else:
        #     bot.send_message(message.from_user.id, 'Спасибо, записал. Сколько фотографий показать (не более 10)')
    else:
        bot.send_message(message.from_user.id, 'Неизвестная команда')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = ''

# @bot.message_handler(state=UserInfoState.need_photo)
# def get_qty_photo(message: Message) -> None:
#     if message.text.isdigit() and int(message.text) in range(1, 11):
#             bot.send_message(message.from_user.id, 'Спасибо, записал. Выбираю лучшие предложенияДА')
#
#             with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#                 data['qty_photo'] = message.text
#
#     else:
#         bot.send_message(message.from_user.id, 'Введите цифрами сколько фотографий показать и не более 10')
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['qty_photo'] = ''







    # get_hotels.get_hotel(message=message)

    # @bot.message_handler(state=UserInfoState.need_photo)
    # def get_need_photo(message: Message) -> None:
    curr_city = get_meta_data.list_cities(user_country=data['city'])

    try:
        lst_hotels = get_meta_data.list_hotels(user_city=curr_city[0][1],
                                               qty_hotels=data['qty_hotels'],
                                               checkIn=data['data_check_in'],
                                               checkOut=data['data_check_out'])
        for hotels in lst_hotels:
            url_hotel = f'https://www.hotels.com/ho{hotels[1]}'
            bot.send_message(message.from_user.id, f'Название отеля: {hotels[0]}'
                                                   f'\nЦена за сутки: {hotels[2]} руб'
                                                   f'\nСсылка на отель: {url_hotel}')
            if data['need_photo'] == 'Да':
                lst_photo = get_meta_data.list_photo(value=hotels[1])#, qty_photo=data['qty_photo'])
                for photo in lst_photo:
                    bot.send_photo(message.from_user.id, photo)
        raise StopIteration
    except StopIteration:
        (bot.send_message(message.from_user.id, 'Вернутся в главное меня.\n/start'))
        bot.delete_state(message.from_user.id, message.chat.id)

    except IndexError:
        bot.send_message(message.from_user.id, 'Поиск не удался. Попробуйте выбрать другой город.\n/start')
        bot.delete_state(message.from_user.id, message.chat.id)


