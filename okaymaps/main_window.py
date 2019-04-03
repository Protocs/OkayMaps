from PyQt5.QtWidgets import QMainWindow
from .config import *
from .map import Map, get_image
from PyQt5 import uic, QtCore


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(WINDOW_PATH, self)
        self.map_widget = Map(self.map)

    def keyReleaseEvent(self, event):
        key = event.key()
        changing = 0.0001 * (1.75 ** (19 - self.map_widget.z))
        print(key)

        if key == QtCore.Qt.Key_PageUp and self.map_widget.z < 19:
            self.map_widget.z += 1
            self.map_widget.set_image(get_image(self.map_widget))

        if key == QtCore.Qt.Key_PageDown and self.map_widget.z > 0:
            self.map_widget.z -= 1
            self.map_widget.set_image(get_image(self.map_widget))

        if key == 87 and self.map_widget.coordinates[1] + changing < 85:
            self.map_widget.coordinates[1] += changing
            self.map_widget.set_image(get_image(self.map_widget))

        if key == 83 and self.map_widget.coordinates[1] - changing > -85:
            self.map_widget.coordinates[1] -= changing
            self.map_widget.set_image(get_image(self.map_widget))

        if key == 68 and self.map_widget.coordinates[0] + changing < 175:
            self.map_widget.coordinates[0] += changing
            self.map_widget.set_image(get_image(self.map_widget))

        if key == 65 and self.map_widget.coordinates[0] - changing > -175:
            self.map_widget.coordinates[0] -= changing
            self.map_widget.set_image(get_image(self.map_widget))
