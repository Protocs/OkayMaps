from PyQt5.QtWidgets import QMainWindow
from .config import *
from .map import Map
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(WINDOW_PATH, self)
        self.map_widget = Map(self.map)
