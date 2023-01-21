import json
import requests
import re
from config_data import config
from typing import Any, Generator
from datetime import date, timedelta

url_country = "https://hotels4.p.rapidapi.com/get-meta-data"
url_cities = "https://hotels4.p.rapidapi.com/locations/search"
url_hotels = "https://hotels4.p.rapidapi.com/properties/list"
url_photo = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"


def list_country() -> list[list[int | Any]]:
    response = requests.request("GET", url_country, headers=config.HAEDERS_RAPID)
    data = json.loads(response.text)
    lst_country = [[i_country["name"], 0] for i_country in data if not re.findall(r'_', i_country["name"])]
    return lst_country


def list_cities(user_country: str = None) -> Generator[tuple[Any, Any], Any, None] | list[str]:
    querystring = {"query": user_country, "locale": "en_EN"}
    response = requests.request("GET", url_cities, headers=config.HAEDERS_RAPID, params=querystring)
    data = json.loads(response.text)

    lst_city = []
    country = str(data['term'])
    if data['suggestions'][0]['group'] == 'CITY_GROUP':
        lst_city = [(i_city['name'], i_city['destinationId'])
                    for i_city in data['suggestions'][0]['entities']
                    if country.capitalize() in i_city['caption']]
    return lst_city


def list_hotels(user_city: str,
                qty_hotels: str = '10',
                checkIn=date.today(),
                checkOut=date.today() + timedelta(days=1)) -> list[tuple[Any, Any, Any, Any]]:

    querystring = {"destinationId": user_city,
                   "pageNumber": "1",
                   "pageSize": qty_hotels,
                   "checkIn": checkIn,
                   "checkOut": checkOut,
                   "adults1": "1",
                   "sortOrder": "PRICE",
                   "locale": "en_EN",
                   "currency": "RUB"}

    response = requests.request("GET", url_hotels, headers=config.HAEDERS_RAPID, params=querystring)
    lst_hotel = [' ']
    dict_data = json.loads(response.text)
    lst_hotel = [(i_hotels['name'],
                  i_hotels['id'],
                  i_hotels['ratePlan']['price']['exactCurrent'],
                  i_hotels['landmarks'][0]['distance'])
                 for i_hotels in dict_data['data']['body']['searchResults']['results']]
    return lst_hotel


def list_photo(value: str, qty_photo: str = '4') -> list[str]:
    querystring = {"id": value}
    response = requests.request("GET", url_photo, headers=config.HAEDERS_RAPID, params=querystring)
    data = json.loads(response.text)
    lst_photo = []
    for photo_url in data["hotelImages"]:
        lst_photo.append(str(photo_url['baseUrl']).replace('_{size}', ''))
        if len(lst_photo) == int(qty_photo):
            break
    return lst_photo
