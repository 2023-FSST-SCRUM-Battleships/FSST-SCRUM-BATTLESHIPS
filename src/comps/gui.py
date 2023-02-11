from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
FIELD_SIZE = 5


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()

        # children
        self.game_layout = GameLayout(self)
        self.stats_layout = StatsLayout(self)

    def ui(self):
        self.setWindowTitle("Titanic who-ooo")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setContentsMargins(20, 20, 20, 20)

    def run(self):
        self.ui()

        self.run_layouts()

        main_widget = QWidget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

    def run_layouts(self):
        self.game_layout.run()
        self.stats_layout.run()


class GameLayout(QVBoxLayout):
    def __init__(self, parent: MainWindow):
        super().__init__()
        self.parent: MainWindow = parent
        self.layout = QVBoxLayout()

        # children
        self.player_buttons_grid_layout = PlayerGridLayout(self)
        self.enemy_buttons_grid_layout = EnemyGridLayout(self)

    def run(self):
        label = QLabel("Game Field")
        self.layout.addWidget(label)

        label = QLabel("Player")
        self.layout.addWidget(label)
        self.player_buttons_grid_layout.run()

        label = QLabel("Enemy")
        self.layout.addWidget(label)
        self.enemy_buttons_grid_layout.run()

        self.parent.layout.addLayout(self.layout)


class PlayerGridLayout(QGridLayout):
    def __init__(self, parent: GameLayout):
        super().__init__()
        self.parent: GameLayout = parent
        self.buttons = []
        self.layout = QGridLayout()

    def run(self):
        self.render_button_layout()

    def render_button_layout(self):
        self.layout.setSpacing(5)

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                button = QPushButton(f"{i, j}")
                self.buttons.append([i, j, button])
                self.layout.addWidget(button, i, j)

        self.parent.layout.addLayout(self.layout)


class EnemyGridLayout(QGridLayout):
    def __init__(self, parent: GameLayout):
        super().__init__()
        self.parent: GameLayout = parent
        self.buttons = []
        self.layout = QGridLayout()

    def run(self):
        self.render_button_layout()

    def render_button_layout(self):
        self.layout.setSpacing(5)

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                button = QPushButton(f"{i, j}")
                self.buttons.append([i, j, button])
                self.layout.addWidget(button, i, j)

        self.parent.layout.addLayout(self.layout)


class StatsLayout(QVBoxLayout):
    def __init__(self, parent: MainWindow):
        super().__init__()
        self.parent: MainWindow = parent
        self.layout = QVBoxLayout()

    def run(self):
        label = QLabel("Player-Stats")
        self.layout.addWidget(label)

        self.parent.layout.addLayout(self.layout)


# todo: later = class Color is needed to display if a shot was correct or incorrect (red / gray)
class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
