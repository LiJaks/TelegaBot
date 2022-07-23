from loader import bot
from telebot.types import Message



# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(message, "TravelMax - это бот-помощник, к сожалению, у него нет достаточного количества знаний, чтобы общаться на эту тему. Для ознакомления с возможностями введите команду /help.")
