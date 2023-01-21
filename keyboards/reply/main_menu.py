from telebot import types
from telebot.types import Message, ReplyKeyboardMarkup
from loader import bot


def bot_start(message: Message) -> ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)#, one_time_keyboard=True)
    low_price = types.KeyboardButton('Узнать топ самых дешёвых отелей в городе')
    high_price = types.KeyboardButton('Узнать топ самых дорогих отелей в городе')
    best_deal = types.KeyboardButton(
        'Узнать топ отелей, наиболее подходящих по цене и расположению от центра')
    history = types.KeyboardButton('Узнать историю поиска отелей')
    markup.add(low_price, high_price, best_deal, history)
    bot.send_message(message.chat.id, f'''Приветствую Вас {message.from_user.first_name}.
Меня зовут *****.
Я помогу Вам выбрать наилучший отель для незабываемого отдыха.''' , reply_markup=markup)
    return markup
