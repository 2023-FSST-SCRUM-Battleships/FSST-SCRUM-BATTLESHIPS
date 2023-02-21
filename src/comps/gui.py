from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
FIELD_SIZE = 12

ROTATION_MAP = [
    lambda x, y: (x, y),
    lambda x, y: (y, x),
    lambda x, y: (-x, -y),
    lambda x, y: (-y, -x),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()

        # children
        self.game_layout = GameLayout(self)
        self.stats_layout = StatsLayout(self)

    def ui(self):
        self.setWindowTitle("Titanic who-ooo")
        # self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setContentsMargins(20, 0, 20, 0)

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


# hardcoded for testing "Ship"
ship_uuid: int = 0
ship_form: list[list[int, int]] = [[0, 0], [1, 0], [2, 0], [1, 1], [2, 1], [3, 1]]
ship_coordinates: list[int, int, int] = [5, 5, 1]


class PlayerGridLayout(QGridLayout):
    def __init__(self, parent: GameLayout):
        super().__init__()
        self.parent: GameLayout = parent
        self.buttons: list[list[list[int, int], object]] = []
        self.layout = QGridLayout()

        # children
        self.ship = Ship(self, ship_uuid, ship_form, ship_coordinates)

    def run(self):
        self.render_button_layout()
        self.ship.run()

    def render_button_layout(self):
        self.layout.setSpacing(1)

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                # button = QPushButton(f"{i, j}")
                button = QPushButton()
                self.buttons.append([[i, j], button])
                self.layout.addWidget(button, i, j)

        # [print(ele) for ele in self.buttons]
        self.parent.layout.addLayout(self.layout)

    # def display_placed_ship(self):


class Ship:
    def __init__(self, parent: PlayerGridLayout, uuid: int, form: list[list[int, int]],
                 root_coordinate: list[int, int, int]):
        super().__init__()
        self.parent: PlayerGridLayout = parent

        self.uuid: int = uuid
        self.form: list[list[int, int]] = form
        self.root_coordinate: list[int, int, int] = root_coordinate
        self.coordinates: list[list[int]] = []

    def run(self):
        # print(f"root-coordinates: {self.root_coordinate}")
        self.get_coordinates_with_rotation()
        self.place_ship()

    def get_coordinates_with_rotation(self):
        for element in self.form:
            relative_x, relative_y = (ele for ele in element)
            relative_x, relative_y = ROTATION_MAP[self.root_coordinate[2]](relative_x, relative_y)
            self.coordinates.append([self.root_coordinate[1] + relative_y, self.root_coordinate[0] + relative_x])

        # print(f"coordinates: {self.coordinates}")

    def place_ship(self):
        # [print(ele[0]) for ele in self.parent.buttons]
        for element in self.parent.buttons:
            for ele in self.coordinates:
                if element[0] == ele:
                    # print(element[0], ele)
                    element[1].setStyleSheet("background-color: red")


class EnemyGridLayout(QGridLayout):
    def __init__(self, parent: GameLayout):
        super().__init__()
        self.parent: GameLayout = parent
        self.buttons: list[list[int, int, object]] = []
        self.layout = QGridLayout()

    def run(self):
        self.render_button_layout()

    def render_button_layout(self):
        self.layout.setSpacing(1)

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                # button = QPushButton(f"{i, j}")
                button = QPushButton()
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
