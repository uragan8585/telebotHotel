from telebot import types, Any
from telebot.types import Message
from handlers.custom_handlers import best_deal, low_price, history, high_price
from loader import bot
from keyboards.reply import main_menu

@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    main_menu.bot_start(message=message)



@bot.message_handler(content_types=['text'])
def bot_message(message: Message) -> Any:
    if message.chat.type == 'private':
        if message.text == 'Узнать топ самых дешёвых отелей в городе':
            low_price.start_survey(message=message)
        elif message.text == 'Узнать топ самых дорогих отелей в городе':
            high_price.start_survey(message=message)
        elif message.text == 'Узнать топ отелей, наиболее подходящих по цене и расположению от центра':
            best_deal.func_bestdeal(message=message)
        elif message.text == 'Узнать историю поиска отелей':
            history.func_history(message=message)
        # else:
        #     bot.send_message(message.chat.id, 'Недопустимая команда.\nИспользуйте команду /start')
