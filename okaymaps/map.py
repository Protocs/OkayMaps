from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from .utils import *


class Map:
    def __init__(self, graphics_view):
        self.graphics_view = graphics_view
        # Текущие координаты карты
        self.coordinates = [58.977707, 53.404967]

        self.z = 16
        self.l = "map"

        self.set_image(get_image(self))

    @property
    def geocoder_params(self):
        return {"geocode": coordinates_to_request(self.coordinates),
                "format": "json"}

    @property
    def static_maps_params(self):
        return {"ll": coordinates_to_request(self.coordinates),
                "l": self.l,
                "z": self.z}

    def set_image(self, image):
        scene = QGraphicsScene()
        self.graphics_view.setScene(scene)
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(image))
        scene.addItem(QGraphicsPixmapItem(pixmap))

    def set_map(self, map_type):
        self.l = map_type
        self.set_image(get_image(self))
