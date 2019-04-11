from PyQt5.QtWidgets import QMainWindow
from math import cos

from .config import *
from .utils import find_object, LongLat, request, ORGANISATION_SEARCH_SERVER
from .map import Map
from PyQt5 import uic, QtCore
from .distance import lonlat_distance


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(WINDOW_PATH, self)
        self.map_widget = Map(self.map, self)
        self.scheme_btn.clicked.connect(lambda: self.map_widget.set_map("map"))
        self.satellite_btn.clicked.connect(lambda: self.map_widget.set_map("sat"))
        self.hybrid_btn.clicked.connect(lambda: self.map_widget.set_map("skl"))

        self.reset_btn.clicked.connect(self.reset_result)
        self.search_btn.clicked.connect(self.search_result)

        self.index_checkbox.stateChanged.connect(self.add_or_remove_postal_index)

    def keyReleaseEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_PageUp:
            self.map_widget.z += 1

        if key == QtCore.Qt.Key_PageDown:
            self.map_widget.z -= 1

        if key == QtCore.Qt.Key_Up:
            self.map_widget.coordinates.lat += self.map_widget.move_offset

        if key == QtCore.Qt.Key_Down:
            self.map_widget.coordinates.lat -= self.map_widget.move_offset

        # Умножаем изменение координат на два, потому что широта ∈ [-90, 90],
        # из-за чего пролистывание происходит в два раза быстрее по сравнению с долготой
        if key == QtCore.Qt.Key_Right:
            self.map_widget.coordinates.long += self.map_widget.move_offset * 2

        if key == QtCore.Qt.Key_Left:
            self.map_widget.coordinates.long -= self.map_widget.move_offset * 2

    def mousePressEvent(self, event):
        x_mouse = event.pos().x()
        y_mouse = event.pos().y()

        x_center = 322
        y_center = 220
        x_offset = x_center - x_mouse
        y_offset = y_center - y_mouse

        x = self.map_widget.coordinates.long - x_offset * 360 / (
                2 ** (self.map_widget.z + 8))
        y = self.map_widget.coordinates.lat + (y_offset + 30) * 220 / (
                2 ** (self.map_widget.z + 8))

        if event.button() == QtCore.Qt.LeftButton:
            self.left_click(x, y)
        elif event.button() == QtCore.Qt.RightButton:
            self.right_click(x, y)

    def left_click(self, x, y):
        mark = LongLat(x, y, self.map_widget)
        self.map_widget.mark = mark
        gcmd = find_object(str(mark))["metaDataProperty"]["GeocoderMetaData"]
        self.map_widget._last_address = gcmd["text"]
        print(gcmd)
        self.map_widget._last_postal = gcmd["Address"].get("postal_code", " - ")
        if self.index_checkbox.isChecked():
            self.full_address.setText(
                gcmd["text"] + ", " + gcmd["Address"].get("postal_code", " - "))
        else:
            self.full_address.setText(gcmd["text"])
        self.map_widget.upd_image()

    def right_click(self, x, y):
        parameters = {"ll": str(round(x, 6)) + "," + str(round(y, 6)),
                      "spn": "0.0008,0.000003",
                      "type": "biz",
                      "format": "json",
                      "results": 500,
                      "apikey": "d890f456-7c66-4912-80cc-5476d1d0b58e",
                      "lang": "ru_RU"}
        response = request(ORGANISATION_SEARCH_SERVER, parameters)
        organizations = response.json()["features"]
        close_organization = {}
        for org in organizations:
            distance = lonlat_distance((x, y), org["geometry"]["coordinates"])
            if distance < close_organization.get("distance", distance + 1):
                close_organization = {"distance": distance,
                                      "name": org["properties"]["name"],
                                      "point": org["geometry"]["coordinates"]}
        self.map_widget.mark = None
        self.map_widget._last_address = None
        self.map_widget._last_postal = None
        self.map_widget.upd_image()
        if not close_organization or close_organization["distance"] > 50:
            self.map_widget.full_address = ""
            return
        self.map_widget.full_address = close_organization["name"]

    def add_or_remove_postal_index(self, state):
        if self.map_widget._last_address is None:
            return
        if state == QtCore.Qt.Checked:
            self.full_address.setText(
                self.map_widget._last_address + ", " + self.map_widget._last_postal)
        else:
            self.full_address.setText(self.map_widget._last_address)

    def search_result(self):
        address = self.search_text.toPlainText()
        result = find_object(address)
        if result:
            coords = LongLat(
                *map(float, result["Point"]["pos"].split()), self.map_widget
            )
            data = result["metaDataProperty"]["GeocoderMetaData"]
            full_address = data["AddressDetails"]["Country"]["AddressLine"]
            print(data)
            self.map_widget.coordinates = coords
            self.map_widget.mark = coords.copy()
            self.map_widget.full_address = full_address
            self.map_widget._last_address = full_address
            self.map_widget._last_address = data["Address"].get("postal_code", " - ")
            if self.index_checkbox.isChecked():
                self.full_address.setText(
                    data["text"] + ", " + data["Address"].get("postal_code", " - "))
            else:
                self.full_address.setText(data["text"])
            self.map_widget.upd_image()

    def reset_result(self):
        self.map_widget.mark = None
        self.map_widget.full_address = None
        self.map_widget.upd_image()
