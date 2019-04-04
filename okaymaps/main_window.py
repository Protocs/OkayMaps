from PyQt5.QtWidgets import QMainWindow
from .config import *
from .utils import find_object, LongLat
from .map import Map
from PyQt5 import uic, QtCore


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(WINDOW_PATH, self)
        self.map_widget = Map(self.map)
        self.scheme_btn.clicked.connect(lambda: self.map_widget.set_map("map"))
        self.satellite_btn.clicked.connect(lambda: self.map_widget.set_map("sat"))
        self.hybrid_btn.clicked.connect(lambda: self.map_widget.set_map("skl"))

        self.search_btn.clicked.connect(self.search_result)

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

    def search_result(self):
        address = self.search_text.toPlainText()
        result = find_object(address)
        if result:
            coords = LongLat(
                *map(float, result["Point"]["pos"].split()), self.map_widget
            )
            self.map_widget.coordinates = coords
            self.map_widget.mark = coords.copy()
            self.map_widget.upd_image()
