import sys

import requests
from PyQt5 import QtCore

GEOCODER_SERVER = "http://geocode-maps.yandex.ru/1.x/"
STATIC_API_SERVER = "http://static-maps.yandex.ru/1.x/"

TRIGGER_BUTTONS = [
    QtCore.Qt.Key_PageUp,
    QtCore.Qt.Key_PageDown,
    QtCore.Qt.Key_Up,
    QtCore.Qt.Key_Down,
    QtCore.Qt.Key_Right,
    QtCore.Qt.Key_Left,
]


def request(server, params):
    try:
        response = requests.get(server, params=params)
        if not response:
            print("Ошибка выполнения запроса:", params)
            print("HTTP статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        return response
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)


def coordinates_to_request(coordinates):
    return ",".join(map(str, coordinates))


def find_object(address):
    params = {"geocode": address, "format": "json"}
    response = request(GEOCODER_SERVER, params).json()["response"]
    if response["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"][
        "found"] != "0":
        return response["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


def pt_to_request(coordinates):
    return ",".join([coordinates_to_request(coordinates), "pm2rdm"])
