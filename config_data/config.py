import os

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
HAEDERS_RAPID: dict[str, str] = {
    "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}
DEFAULT_COMMANDS = ('start', "Запустить бота")
# DEFAULT_COMMANDS = (
#     ('start', "Запустить бота")
#     ('help', "Вывести справку")
#     ('survey', "Опрос")
# )
