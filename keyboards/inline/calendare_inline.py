from loader import bot
from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, timedelta
import time
from states.user_state import UserState


def get_calendar(is_process=False, callback_data=None, **kwargs):
    if is_process:
        result, key, step = DetailedTelegramCalendar(calendar_id=kwargs['calendar_id'],
                                                     current_date=kwargs.get('current_date'),
                                                     min_date=kwargs['min_date'],
                                                     max_date=kwargs['max_date'],
                                                     locale=kwargs['locale']).process(callback_data.data)
        return result, key, step
    else:
        calendar, step = DetailedTelegramCalendar(calendar_id=kwargs['calendar_id'],
                                                  current_date=kwargs.get('current_date'),
                                                  min_date=kwargs['min_date'],
                                                  max_date=kwargs['max_date'],
                                                  locale=kwargs['locale']).build()
        return calendar, step

ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'} # Пригодится чтобы русифицировать сообщения

def calendar_command(message: Message) -> None:
    today = date.today()
    calendar, step = get_calendar(calendar_id=1,
                                  current_date=today,
                                  min_date=today, # Старые даты отбрасываем они нас навряд ли интересуют
                                  max_date=today + timedelta(days=365), # Чтобы максимальное значение дат было +1 год
                                  locale="ru")
    bot.send_message(message.chat.id, f"Выберите {ALL_STEPS[step]}", reply_markup=calendar)
    bot.set_state(message.from_user.id, UserState.accept_year, message.chat.id)

@bot.callback_query_handler(state=UserState.accept_year, func=None)
def check_city_selected(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text:
            bot.send_message(message.chat.id, 'Ввод невозможен. Пожалуйста, выберите вариант из предложенных.')
        else:
            data['check_year'] = True
            bot.set_state(message.from_user.id, UserState.accept_date, message.chat.id)

@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def handle_date_in(call: CallbackQuery):
    today = date.today()
    result, key, step = get_calendar(calendar_id=1,
                                     current_date=today,
                                     min_date=today,
                                     max_date=today + timedelta(days=365),
                                     locale="ru",
                                     is_process=True,
                                     callback_data=call)
    if not result and key:
        # Продолжаем отсылать шаги, пока не выберут дату "result"
        bot.edit_message_text(f"Выберите {ALL_STEPS[step]}",
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['date_in'] = result  # Дата выбрана, сохраняем ее

            bot.edit_message_text(f"Дата заезда: {result}",
                                  call.message.chat.id,
                                  call.message.message_id)

            bot.send_message(call.message.chat.id, "Выберите дату выезда")
            # И здесь сразу используем вновь полученные данные и генерируем новый календарь
            calendar, step = get_calendar(calendar_id=2,
                                          min_date=result + timedelta(days=1),
                                          max_date=result + timedelta(days=365),
                                          locale="ru",
                                          )

            bot.send_message(call.from_user.id,
                             f"Выберите {ALL_STEPS[step]}",
                             reply_markup=calendar)
            bot.set_state(call.from_user.id, UserState.date_in, call.message.chat.id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def handle_date_out(call: CallbackQuery):
    today = date.today()
    result, key, step = get_calendar(calendar_id=2,
                                     current_date=today,
                                     min_date=today,
                                     max_date=today + timedelta(days=365),
                                     locale="ru",
                                     is_process=True,
                                     callback_data=call)
    if not result and key:
        # Продолжаем отсылать шаги, пока не выберут дату "result"
        bot.edit_message_text(f"Выберите {ALL_STEPS[step]}",
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            if result > data['date_in']:
                data['date_out'] = result  # Дата выбрана, сохраняем ее
                bot.edit_message_text(f"Дата выезда {result}",
                                      call.message.chat.id,
                                      call.message.message_id)
                bot.send_message(call.from_user.id, 'Сколько предложений отелей вывести? (макс.25)')
                bot.set_state(call.from_user.id, UserState.hotels_count, call.message.chat.id)
            else:
                del_mes = bot.send_message(call.message.chat.id, 'Дата выезда не может быть раньше, чем дата заезда. Пожалуйста, повторите попытку.')
                time.sleep(3)
                bot.delete_message(call.message.chat.id, del_mes.message_id)
