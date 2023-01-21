from loader import bot
from telebot.types import Message


def func_history(message: Message):
    bot.send_message(message.chat.id, 'Тут будет функция history')
