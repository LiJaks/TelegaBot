import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены, т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

DEFAULT_COMMANDS = (
    ('hello', "Приветствие и знакомство с ботом"),
    ('help', "Список всех доступных команд для общения с ботом"),
    ('lowprice', "Список отелей с низкой ценой"),
    ('highprice', "Список отелей с высокой ценой"),
    ('bestdeal', "Список отелей подходящих по цене и расположению от центра"),
    ('history', "История поиска отелей"),
)
