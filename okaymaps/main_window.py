from PyQt5.QtWidgets import QMainWindow
from .config import *
from .utils import TRIGGER_BUTTONS, find_object
from .map import Map
from PyQt5 import uic, QtCore


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(WINDOW_PATH, self)
        self.map_widget = Map(self.map)
        self.scheme_btn.clicked.connect(lambda: self.map_widget.set_map("map"))
        self.sputnik_btn.clicked.connect(lambda: self.map_widget.set_map("sat"))
        self.hybrid_btn.clicked.connect(lambda: self.map_widget.set_map("skl"))

        self.search_btn.clicked.connect(self.search_result)

    def keyReleaseEvent(self, event):
        key = event.key()
        if key not in TRIGGER_BUTTONS:
            return

        if key == QtCore.Qt.Key_PageUp and self.map_widget.z < 19:
            self.map_widget.z += 1

        if key == QtCore.Qt.Key_PageDown and self.map_widget.z > 0:
            self.map_widget.z -= 1

        if key == QtCore.Qt.Key_Up and \
                self.map_widget.coordinates[1] + self.map_widget.changing < 85:
            self.map_widget.coordinates[1] += self.map_widget.changing

        if key == QtCore.Qt.Key_Down and \
                self.map_widget.coordinates[1] - self.map_widget.changing > -85:
            self.map_widget.coordinates[1] -= self.map_widget.changing

        # Умножаем изменение координат на два, потому что широта ∈ [-90, 90],
        # из-за чего пролистывание происходит в два раза быстрее по сравнению с долготой
        if key == QtCore.Qt.Key_Right and \
                self.map_widget.coordinates[0] + self.map_widget.changing < 175:
            self.map_widget.coordinates[0] += self.map_widget.changing * 2

        if key == QtCore.Qt.Key_Left and \
                self.map_widget.coordinates[0] - self.map_widget.changing > -175:
            self.map_widget.coordinates[0] -= self.map_widget.changing * 2
        self.map_widget.upd_image()

    def search_result(self):
        address = self.search_text.toPlainText()
        result = find_object(address)
        if result:
            coords = list(map(float, result["Point"]["pos"].split()))
            self.map_widget.coordinates = coords
            self.map_widget.pt = coords.copy()
            self.map_widget.upd_image()
