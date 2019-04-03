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

        self.upd_image()

    @property
    def geocoder_params(self):
        return {"geocode": coordinates_to_request(self.coordinates),
                "format": "json"}

    @property
    def static_maps_params(self):
        return {"ll": coordinates_to_request(self.coordinates),
                "l": self.l,
                "z": self.z}

    @property
    def image(self):
        return request(STATIC_API_SERVER, self.static_maps_params).content

    @property
    def changing(self):
        return 0.0001 * (1.75 ** (19 - self.z))

    def upd_image(self):
        scene = QGraphicsScene()
        self.graphics_view.setScene(scene)
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(self.image))
        scene.addItem(QGraphicsPixmapItem(pixmap))

    def set_map(self, map_type):
        self.l = map_type
        self.upd_image()
