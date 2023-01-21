from loader import bot
from telebot.types import Message


def func_bestdeal(message: Message):
    bot.send_message(message.chat.id, 'Тут будет функция bestdeal')
