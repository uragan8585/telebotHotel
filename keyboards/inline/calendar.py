"""
Simple time range limit.
"""

from datetime import date
from loader import bot
from telebot.types import Message, CallbackQuery
from telegram_bot_calendar.detailed import DetailedTelegramCalendar, DAY, LSTEP


class WMonthTelegramCalendar(DetailedTelegramCalendar):
    first_step = DAY
    prev_button = '⬅️'
    next_button = '➡️'


def start(message: Message):
    calendar, step = WMonthTelegramCalendar(locale='ru', min_date=date.today()).build()
    bot.send_message(message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=WMonthTelegramCalendar.func())
def call(call: CallbackQuery):
    result, key, step = WMonthTelegramCalendar(locale='ru', min_date=date.today()).process(call.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(result,
                              call.message.chat.id,
                              call.message.message_id)
        # bot.send_message(message.message.chat.id, type(result), str(result))
        # return result
