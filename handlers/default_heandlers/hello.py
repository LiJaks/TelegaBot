from telebot.types import Message
from loader import bot

@bot.message_handler(commands=['hello'])
def bot_start(message: Message) -> None:
    bot.send_message(message.chat.id,
                       f'Здравствуйте, {message.from_user.full_name}. Я MaxBot, ваш помощник в поиске отелей! Для ознакомления со всеми доступными возможностями воспользуйтесь командой /help')