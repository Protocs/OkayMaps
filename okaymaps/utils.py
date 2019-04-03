import sys

import requests

GEOCODER_SERVER = "http://geocode-maps.yandex.ru/1.x/"
STATIC_API_SERVER = "http://static-maps.yandex.ru/1.x/"


def request(server, params):
    try:
        response = requests.get(server, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("HTTP статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        return response
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)


def get_image(map_object):
    return request(STATIC_API_SERVER, map_object.params).content

def coordinates_to_request(coordinates):
    return ",".join(map(str, coordinates))