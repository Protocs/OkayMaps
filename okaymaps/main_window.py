from PyQt5.QtWidgets import QMainWindow
from .config import *
from .utils import find_object, LongLat
from .map import Map
from PyQt5 import uic, QtCore


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

        x_center = 316
        y_center = 250
        x_offset = x_center - x_mouse
        y_offset = y_center - y_mouse

        x = self.map_widget.coordinates.long - x_offset * 360 / (
                2 ** (self.map_widget.z + 8))
        y = self.map_widget.coordinates.lat + y_offset * 220 / (
                2 ** (self.map_widget.z + 8))

        mark = LongLat(x, y, self.map_widget)
        self.map_widget.mark = mark
        self.map_widget.upd_image()

    def add_or_remove_postal_index(self, state):
        self.search_result()

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
            if self.index_checkbox.isChecked() and "postal_code" in data["Address"]:
                self.map_widget.full_address += ", " + data["Address"]["postal_code"]
            self.map_widget.upd_image()

    def reset_result(self):
        self.map_widget.mark = None
        self.map_widget.full_address = None
        self.map_widget.upd_image()
