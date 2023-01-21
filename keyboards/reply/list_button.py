from loader import bot
from telebot import types
from telebot.types import Message, ReplyKeyboardMarkup
from typing import Generator, Any


def list_button(message, lts) -> ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    markup.add(*(types.KeyboardButton(i_lst[0]) for i_lst in sorted(lts)))
    bot.send_message(message.chat.id, 'Для примера', reply_markup=markup)
    return markup
