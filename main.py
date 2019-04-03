import sys
from PyQt5.QtWidgets import QApplication
from okaymaps.main_window import MainWindow

FIRST_WINDOW = MainWindow

app = QApplication(sys.argv)

w = FIRST_WINDOW()
w.show()
exit(app.exec())
