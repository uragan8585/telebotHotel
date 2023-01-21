from loader import bot
import handlers
from telebot import custom_filters
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':
    bot.add_custom_filter(custom_filter=StateFilter(bot))
    set_default_commands(bot)
    bot.polling(none_stop=True, interval=0)
