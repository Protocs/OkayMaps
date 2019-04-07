from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from okaymaps.utils import LongLat, request, STATIC_API_SERVER


class Map:
    def __init__(self, graphics_view, window):
        self.graphics_view = graphics_view
        self.parent_window = window

        self._z = 16
        self._draw_mode = "map"
        self.mark = None
        self._full_address = None

        # Текущие координаты карты
        self.coordinates = LongLat(58.977707, 53.404967, self)

        self.upd_image()

    @property
    def z(self):
        return self._z

    @property
    def full_address(self):
        return self._full_address

    @full_address.setter
    def full_address(self, new_address):
        self._full_address = new_address
        self.parent_window.full_address.setText(self.full_address)

    @z.setter
    def z(self, new_z):
        self._z = new_z
        if self._z < 2:
            self._z = 2
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
