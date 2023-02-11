from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout, QBoxLayout

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
FIELD_SIZE = 5


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # children
        self.player_buttons_grid_layout = PlayerGridLayout(self)

    def run(self):
        self.ui()

        self.player_buttons_grid_layout.run()

    def ui(self):
        self.setWindowTitle("Titanic who-ooo")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setContentsMargins(20, 20, 20, 20)


class PlayerGridLayout(QGridLayout):
    def __init__(self, parent: "MainWindow"):
        super().__init__()
        self.parent: "MainWindow" = parent
        self.buttons = []

    def run(self):
        self.render_button_layout()

    def render_button_layout(self):
        layout = QGridLayout()
        layout.setSpacing(0)

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                button = QPushButton(f"{i, j}")
                self.buttons.append([i, j, button])
                layout.addWidget(button, i, j)

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
