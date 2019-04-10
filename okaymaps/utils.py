import requests
from PyQt5 import QtCore

GEOCODER_SERVER = "http://geocode-maps.yandex.ru/1.x/"
STATIC_API_SERVER = "http://static-maps.yandex.ru/1.x/"
ORGANISATION_SEARCH_SERVER = "https://search-maps.yandex.ru/v1/"

TRIGGER_BUTTONS = [
    QtCore.Qt.Key_PageUp,
    QtCore.Qt.Key_PageDown,
    QtCore.Qt.Key_Up,
    QtCore.Qt.Key_Down,
    QtCore.Qt.Key_Right,
    QtCore.Qt.Key_Left,
]

_LAT_RANGE = (-85, 86)
_LONG_RANGE = (-175, 176)


def clamp(val, min_, max_):
    """Ограничивает ``val`` между ``min_`` и ``max_``."""
    return min(max_, max(val, min_))


class LongLat:
    """Широта и долгота.

    Автоматически обновляет карту при изменении.
    """

    def __init__(self, long, lat, map_widget):
        self._map_widget = map_widget
        self._long = long
        self._lat = lat

    @property
    def long(self):
        return self._long

    @long.setter
    def long(self, value):
        self._long = clamp(value, *_LONG_RANGE)
        self._map_widget.upd_image()

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        self._lat = clamp(value, *_LAT_RANGE)
        self._map_widget.upd_image()

    def __str__(self):
        return str(round(self.long, 6)) + "," + str(round(self.lat, 6))

    def copy(self):
        return LongLat(self.long, self.lat, self._map_widget)

    @property
    def mark_str(self):
        return str(self) + ",pm2rdm"


def request(server, params):
    try:
        response = requests.get(server, params=params)
        if not response:
            print("Ошибка выполнения запроса:", params)
            print("HTTP статус:", response.status_code, "(", response.reason, ")")
            exit(1)
        return response
    except ConnectionError:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        exit(1)


def find_object(address):
    params = {"geocode": address, "format": "json"}
    response = request(GEOCODER_SERVER, params).json()["response"]
    geo_obj_collection = response["GeoObjectCollection"]
    grmd = geo_obj_collection["metaDataProperty"]["GeocoderResponseMetaData"]
    if grmd["found"] != "0":
        return response["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
