import sys
import random

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPalette, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QLabel, QPushButton, QMainWindow, \
    QFileDialog, QHBoxLayout, QVBoxLayout, QStackedLayout, QBoxLayout

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # children
        self.buttons_grid_layout = ButtonGridLayout(self)

    def run(self):
        self.ui()
        self.buttons_grid_layout.run()

    def ui(self):
        self.setWindowTitle("Titanic who-ooo")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setContentsMargins(20, 20, 20, 20)


class ButtonGridLayout(QGridLayout):
    def __init__(self, parent: "MainWindow"):
        super().__init__()
        self.parent: "MainWindow" = parent

    def run(self):
        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.parent.setCentralWidget(widget)


class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
