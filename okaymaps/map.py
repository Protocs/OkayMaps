from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from okaymaps.utils import LongLat, request, STATIC_API_SERVER


class Map:
    def __init__(self, graphics_view):
        self.graphics_view = graphics_view

        self._z = 16
        self._draw_mode = "map"
        self.mark = None

        # Текущие координаты карты
        self.coordinates = LongLat(58.977707, 53.404967, self)

        self.upd_image()

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, new_z):
        self._z = new_z
        if self._z < 0:
            self._z = 0
        if self._z > 19:
            self._z = 19

        self.upd_image()

    @property
    def static_maps_params(self):
        params = {"ll": str(self.coordinates),
                  "l": self._draw_mode,
                  "z": self.z}
        if self.mark:
            params.update({"pt": self.mark.mark_str})
        return params

    @property
    def image(self):
        return request(STATIC_API_SERVER, self.static_maps_params).content

    @property
    def move_offset(self):
        return 0.0001 * (1.75 ** (19 - self.z))

    def upd_image(self):
        scene = QGraphicsScene()
        self.graphics_view.setScene(scene)
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(self.image))
        scene.addItem(QGraphicsPixmapItem(pixmap))

    def set_map(self, map_type):
        self._draw_mode = map_type
        self.upd_image()
