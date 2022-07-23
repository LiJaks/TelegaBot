from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):

    city = State()
    accept_city = State()
    accept_year = State()
    accept_date = State()
    date_in = State()
    date_out = State()
    hotels_count = State()
    check_photo = State()
    photo_count = State()
    response = State()
