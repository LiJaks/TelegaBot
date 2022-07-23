import requests
import re
import json

from config_data.config import RAPID_API_KEY
from typing import Dict, Optional



def request_to_api(url: str, querystring: Dict):
    """
    Ф-я проверки статуса ответа при запросе к API

    :param: message: сообщение пользователя
    :param: url: ссылка
    :param: querystring: словарь с данным для получения ответа при запросе к API

    :return: response: json-файл c данными по найденному городу
    :return: None: "отрицательный" код ответа при запросе к API
    """

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=20)
        if response.status_code == 200:
            return response
    except requests.exceptions.ReadTimeout:
        return None

def destination_id(city: str) -> Optional[list]:
    """
    Ф-я осуществляет поиск и проверку наличия названия города, введённого пользователем

    :param: city_check: название города

    :return: cities: список данных (название города, id города)
    :return: None: отсутствие города в списке при запросе к API
    """
    try:
        url = "https://hotels4.p.rapidapi.com/locations/v2/search"
        querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}
        response = request_to_api(url, querystring)
        if response:
            pattern = r'(?<="CITY_GROUP",).+?[\]]'
            find = re.search(pattern, response.text)
            location_info = json.loads(f"{{{find[0]}}}")
            cities_list = list()
            for dest_id in location_info['entities']:
                clear_destination = re.sub(r'[(<][^A-ZА-Яа-я]+[>)]|[(].+', '', dest_id['caption'])
                cities_list.append({'city_name': clear_destination.strip().title(), 'destination_id': dest_id['destinationId']})
            return cities_list
        else:
            return None
    except Exception:
        return None


def hotel_search(sort: str, destinationID: str, date_in: str, date_out: str, num_hotels: str) -> Optional[list]:
    """
    Ф-я осуществляет поиск и проверку наличия отелей в городе

    :param destinationID: id локации для поиска отелей
    :param date_in: дата заезда пользователя
    :param date_out: дата выезда пользователя
    :param num_hotels: количество отелей, которое нужно вывести пользователю
    :return: список с информацией о отелях
    """
    try:
        url = "https://hotels4.p.rapidapi.com/properties/list"
        querystring = {"destinationId": destinationID, "pageNumber": "1", "pageSize": num_hotels, "checkIn": date_in,
                       "checkOut": date_out, "adults1": "1", "sortOrder": sort, "locale": "ru_RU", "currency": "RUB"}
        response = request_to_api(url, querystring)
        if response:
            hotels_info = json.loads(response.text)
            results = hotels_info['data']['body']['searchResults']['results']
            return results
        else:
            return None
    except Exception:
        return None

def photo_hotels(id: str, photo_count: int) -> Optional[list]:
    """
    Ф-я осуществляет поиск и проверку наличия отелей в городе

    :param destinationID: id локации для поиска отелей
    :param date_in: дата заезда пользователя
    :param date_out: дата выезда пользователя
    :param num_hotels: количество отелей, которое нужно вывести пользователю
    :return: список с информацией о отелях
    """

    count = 0
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id":id}
    response = request_to_api(url, querystring)
    if response:
        photo_list = []
        photo_info = json.loads(response.text)
        for elem in photo_info['hotelImages']:
            if count != int(photo_count):
                count += 1
                photo = elem['baseUrl'].replace('{size}', 'w')
                photo_list.append(photo)
            else:
                return photo_list
    else:
        return None
