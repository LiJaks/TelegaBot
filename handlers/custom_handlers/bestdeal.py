from loader import bot
from telebot.types import Message
from states.user_state import UserState


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: Message) -> None:
    """
    Обработка команды /bestdeal

    :param: message
    :return: None
    """

    bot.set_state(message.from_user.id, UserState.city, message.chat.id)
    bot.send_message(message.chat.id, 'В каком городе будет происходить поиск отелей?')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = 'bestdeal'
