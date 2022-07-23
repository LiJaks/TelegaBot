import time
from loader import bot
from telebot.types import Message
from states.user_state import UserState
from rapidapi.rapidapi import destination_id
from keyboards.inline.city_keyboard import city_markup


# condition_low = "PRICE" # критерий поиска отелей от низкой цены

@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    """
    Обработка команды /lowprice

    :param: message
    :return: None
    """

    bot.set_state(message.from_user.id, UserState.city, message.chat.id)
    bot.send_message(message.chat.id, 'В каком городе будет происходить поиск отелей?')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = 'lowprice'


# @bot.message_handler(state=UserState.city)
# def get_city(message: Message) -> None:
#     """
#     Поиск названия города в базе Hotels.com, вывод результатов на inline клавиатуру
#
#     :param: message
#     :return: None
#     """
#
#
#     cities_list = destination_id(message.text)
#     if cities_list is None or not cities_list:
#         bot.send_message(message.chat.id,
#                            f'Город не был найден в списке сайта Hotels.com. Пожалуйста, проверьте корректность введённого названия и повторите попытку ввода.')
#         bot.set_state(message.from_user.id, UserState.city, message.chat.id)
#     else:
#         bot.send_message(message.chat.id, 'Выберите подходящий вариант, нажатием на кнопку:', reply_markup=city_markup(cities_list))
#         bot.set_state(message.from_user.id, UserState.accept_city, message.chat.id)
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['find_cities'] = {'cities': cities_list}
#
#
# @bot.message_handler(state=UserState.accept_city)
# def check_city_selected(message):
#     """
#
#     :param message:
#     :return:
#     """
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         cities = data['find_cities']['cities']
#         del_mes = bot.send_message(message.chat.id, 'Ввод невозможен! Выберите подходящий вариант из перечисленных.')
#         time.sleep(3)
#         bot.delete_message(message.chat.id, del_mes.message_id)
#
#
# @bot.message_handler(state=UserState.hotels_count)
# def hotels_count_func(message: Message) -> None:
#     """
#     Проверка даты въезда
#
#     :param: message
#     :return: None
#     """
#     if message.text.isdigit() and int(message.text) <= 25:
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['hotels_count'] = message.text
#             bot.send_message(message.chat.id, 'Показать фотографии отелей?')
#             bot.set_state(message.from_user.id, UserState.check_photo, message.chat.id)
#     else:
#         bot.send_message(message.chat.id, 'Значение должно быть числом, не превышающее 25-ти. Повторите попытку ввода')
#         bot.set_state(message.from_user.id, UserState.hotels_count, message.chat.id)
#
#
# @bot.message_handler(state=UserState.check_photo)
# def check_photo_func(message: Message) -> None:
#     """
#     Проверка даты въезда
#
#     :param: message
#     :return: None
#     """
#     pos = ['yes', 'да']
#     neg = ['no', 'нет']
#     if message.text in pos:
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['check_photo'] = message.text
#             bot.send_message(message.chat.id, 'Сколько фотографий вывести? (макс.10)')
#             bot.set_state(message.from_user.id, UserState.photo_count, message.chat.id)
#     elif message.text in neg:
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['check_photo'] = message.text
#         final_response(message, condition_low)
#     else:
#         bot.send_message(message.chat.id, 'Ввод возможен либо yes/да или no/нет. Повторите попытку ввода.')
#         bot.set_state(message.from_user.id, UserState.check_photo, message.chat.id)
#
#
# @bot.message_handler(state=UserState.photo_count)
# def photo_count(message: Message) -> None:
#     if message.text.isdigit() and int(message.text) <= 10:
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['photo_count'] = message.text
#         final_response(message, condition_low)
#     else:
#         bot.send_message(message.chat.id, 'Значение должно быть числом, не превышающее 10-ти. Повторите попытку ввода.')
#         bot.set_state(message.from_user.id, UserState.photo_count, message.chat.id)
