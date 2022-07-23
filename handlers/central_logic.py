from loader import bot
from telebot.types import Message, InputMediaPhoto
from states.user_state import UserState
from rapidapi.rapidapi import destination_id, hotel_search, photo_hotels
from keyboards.inline.city_keyboard import city_markup


def sortOrder(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data['command'] == 'highprice':
            sort = "PRICE_HIGHEST_FIRST"
        elif data['command'] == 'lowprice':
            sort = "PRICE"
        elif data['bestdeal'] == 'bestdeal':
            sort = "DISTANCE_FROM_LANDMARK"
        return sort

@bot.message_handler(state=UserState.city)
def get_city(message: Message) -> None:
    """
    Поиск названия города в базе Hotels.com, вывод результатов на inline клавиатуру

    :param: message
    :return: None
    """


    cities_list = destination_id(message.text)
    if cities_list is None or not cities_list:
        bot.send_message(message.chat.id,
                           f'Город не был найден в списке сайта Hotels.com. Пожалуйста, проверьте корректность введённого названия и повторите попытку ввода.')
        bot.set_state(message.from_user.id, UserState.city, message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Выберите подходящий вариант, нажатием на кнопку:', reply_markup=city_markup(cities_list))
        bot.set_state(message.from_user.id, UserState.accept_city, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['find_cities'] = {'cities': cities_list}


@bot.message_handler(state=UserState.accept_city)
def check_city_selected(message: Message):
    """

    :param message:
    :return:
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        cities = data['find_cities']['cities']
        bot.send_message(message.chat.id, 'Ввод невозможен! Выберите подходящий вариант из перечисленных.')


@bot.message_handler(state=UserState.hotels_count)
def hotels_count_func(message: Message) -> None:
    """
    Проверка даты въезда

    :param: message
    :return: None
    """
    if message.text.isdigit() and int(message.text) <= 25:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_count'] = message.text
            bot.send_message(message.chat.id, 'Показать фотографии отелей?')
            bot.set_state(message.from_user.id, UserState.check_photo, message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Значение должно быть числом, не превышающее 25-ти. Повторите попытку ввода')
        bot.set_state(message.from_user.id, UserState.hotels_count, message.chat.id)


@bot.message_handler(state=UserState.check_photo)
def check_photo_func(message: Message) -> None:
    """
    Проверка даты въезда

    :param: message
    :return: None
    """

    pos = ['yes', 'да']
    neg = ['no', 'нет']
    if message.text in pos:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['check_photo'] = message.text
            bot.send_message(message.chat.id, 'Сколько фотографий вывести? (макс.10)')
            bot.set_state(message.from_user.id, UserState.photo_count, message.chat.id)
    elif message.text in neg:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['check_photo'] = message.text
        response_func(message)
    else:
        bot.send_message(message.chat.id, 'Ввод возможен либо yes/да или no/нет. Повторите попытку ввода.')
        bot.set_state(message.from_user.id, UserState.check_photo, message.chat.id)


@bot.message_handler(state=UserState.photo_count)
def photo_count(message: Message) -> None:
    """

    :param message:
    :return:
    """
    if message.text.isdigit() and int(message.text) <= 10:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_count'] = message.text
        response_func(message)
    else:
        bot.send_message(message.chat.id, 'Значение должно быть числом, не превышающее 10-ти. Повторите попытку ввода.')
        bot.set_state(message.from_user.id, UserState.photo_count, message.chat.id)


def response_func(message: Message) -> None:
    """

    :param message:
    :return:
    """

    bot.send_message(message.chat.id, 'Ведётся поиск...')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        sort = sortOrder(message)
        response = hotel_search(sort, data['user_location']['destination_id'], data['date_in'], data['date_out'], data['hotels_count'])
        if response:
            data['find_hotels'] = {'hotels':[list(response)]}

            for hotel in response:
                name_hotel = hotel['name']
                one_d_price = hotel['ratePlan']['price']['current']
                dist_to_center = hotel['landmarks'][0]['distance']
                if 'streetAddress' in hotel['address']:
                    address = hotel['address']['streetAddress']
                else:
                    address = hotel['address']['locality']
                url_hotel = f"www.hotels.com/ho{hotel['id']}"

                days = str(data['date_out'] - data['date_in']).split() # посчитав разницу в днях между заездом и выездом, отделяем именно число дней
                only_price = int(one_d_price.rstrip(' RUB').replace(',', '')) # отделяем числовое значение цены и убираем запятую для дальнейших расчётов
                full_price = int(days[0])*only_price # высчитываем полную цену за количество указанных дней

                bot.send_message(message.chat.id, '<b>Название:</b> <i>{name_hotel}</i>'
                                                '\n<b>Адрес:</b> <i>{address}</i>'
                                                '\n<b>Удалённость от центра:</b> <i>{dist_to_center}</i>'
                                                '\n<b>Цена за один день проживания:</b> <i>{one_d_price}</i>'
                                                '\n<b>Цена за указанный период:</b> <i>{full_price:,d} RUB</i>'
                                                '\n<b>Ссылка на отель:</b> <i>{url_hotel}</i>'.format(name_hotel=name_hotel,
                                                                                                                       address=address,
                                                                                                                       dist_to_center=dist_to_center,
                                                                                                                       one_d_price=one_d_price,
                                                                                                                       full_price=full_price,
                                                                                                                       url_hotel = url_hotel), parse_mode = 'HTML')
                if data['check_photo'] == 'yes' or data['check_photo'] == 'да':
                    photo_list = photo_hotels(hotel['id'], data['photo_count'])
                    if photo_list is None or not photo_list:
                        bot.send_message(message.chat.id, 'Фотографии отеля не найдены.')
                    else:
                        media = []
                        for photo in photo_list:
                            media.append(InputMediaPhoto(photo))
                        bot.send_media_group(message.chat.id, media)
            bot.reset_data(user_id=message.from_user.id)
            bot.delete_state(user_id=message.from_user.id)
        else:
            bot.send_message(message.chat.id,
                             'К сожалению, информация о отелях не найдена. Пожалуйста, проверьте введённые данные и повторите попытку.')
            bot.reset_data(user_id=message.from_user.id)
            bot.delete_state(user_id=message.from_user.id)