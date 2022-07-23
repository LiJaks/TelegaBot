from loader import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards.inline.calendare_inline import calendar_command
from states.user_state import UserState



def city_markup(cities_list):
    """
    Создание inline-keyboard для выбора локации

    :param cities_list: список локаций, подходящих по названию, которое ввёл пользователь
    :return: возвращает inline-keyboard
    """
    destinations = InlineKeyboardMarkup()
    for city in cities_list:
        destinations.add(InlineKeyboardButton(text=city['city_name'], callback_data=(f'{city["destination_id"]}')))
    return destinations


@bot.callback_query_handler(func=lambda call: True)
def location(call: CallbackQuery) -> None:
    """
    Обработка, выбранной пользователем, кнопки на клавиатуре

    :param: call
    :return: None
    """
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        for local in data['find_cities']['cities']:
            if call.data == local['destination_id']:
                data['user_location'] = local
                bot.edit_message_text(f"Ваш выбор: {local['city_name']}",
                                      call.message.chat.id,
                                      call.message.message_id)
                break
    calendar_command(call.message)
    bot.set_state(call.from_user.id, UserState.hotels_count, call.message.chat.id)