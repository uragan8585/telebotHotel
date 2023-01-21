from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_contact() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(True, True)
    markup.add(KeyboardButton('Отправить контакт', request_contact=True))
    return markup
