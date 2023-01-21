from loader import bot
from telebot import types
from telebot.types import Message
from states.contact_information import UserInfoState
from api_requests import get_meta_data
from keyboards.reply import list_button
from keyboards.inline import calendar
from datetime import datetime
from utils import get_hotels


@bot.message_handler(commands=['high_price'])
def high_price(message: Message) -> None:
    bot.send_message(message.chat.id, 'Тут будет функция history')