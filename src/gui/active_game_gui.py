from functools import partial

from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel

WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 400
FIELD_SIZE: int = 12

ROTATION_MAP = [
    lambda x, y: [x, y],
    lambda x, y: [y, x],
    lambda x, y: [-x, -y],
    lambda x, y: [-y, -x],
]

SHIP_BUTTONS: list[str] = [
    "<-",
    "rotate left",
    "rotate right",
    "->",
]

PLACED_SHIPS: list[[int, [[int, int], [int, int, int]]]] = []
USED_COORDINATES: list[[int, int]] = []


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


class PlayerGridLayout(QGridLayout):
    def __init__(self, parent: GameLayout):
        super().__init__()
        self.parent: GameLayout = parent
        self.buttons: list[[[int, int], object]] = []
        self.layout = QGridLayout()

        # children

    def run(self):
        self.render_button_layout()

    def render_button_layout(self):
        self.layout.setSpacing(1)

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                # button = QPushButton(f"{i, j}")
                button = QPushButton()
                button.setFixedSize(25, 25)

                self.buttons.append([[i, j], button])
                self.layout.addWidget(button, i, j)

        # [print(ele) for ele in self.buttons]
        self.parent.layout.addLayout(self.layout)

    # def display_placed_ship(self):


class Ship:
    def __init__(self, parent: PlayerGridLayout, uuid: int, form: list[[int, int]],
                 root_coordinates: list[int, int, int]):
        super().__init__()
        self.parent: PlayerGridLayout = parent

        # self.ships: list[list[int, list[list[int, int]], list[int, int, int]]] = ships
        self.uuid: int = uuid
        self.form: list[[int, int]] = form
        self.root_coordinate: list[int, int, int] = root_coordinates
        self.coordinates: list[[int]] = []

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
        # var = [[[[element[1].setStyleSheet("background-color: red"), print("hello")] if element[0] == ele else ""]
        #         for ele in self.coordinates] for element in self.parent.buttons]

        for element in self.parent.buttons:
            for ele in self.coordinates:
                if element[0] == ele:
                    element[1].setStyleSheet("background-color: red")


class EnemyGridLayout(QGridLayout):
    def __init__(self, parent: GameLayout):
        super().__init__()
        self.parent: GameLayout = parent
        self.buttons: list[[[int, int], object]] = []
        self.layout = QGridLayout()

    def run(self):
        self.render_button_layout()
        self.connect_buttons()

    def render_button_layout(self):
        self.layout.setSpacing(1)

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                # button = QPushButton(f"{i, j}")
                button = QPushButton()
                button.setFixedSize(25, 25)

                self.buttons.append([[i, j], button])
                self.layout.addWidget(button, i, j)

        self.parent.layout.addLayout(self.layout)

    def connect_buttons(self):
        for ele in self.buttons:
            ele[1].clicked.connect(partial(self.handle_clicked_button, ele[0], ele[1]))
            print(ele)

    def handle_clicked_button(self, coordinates: list[int, int], button: QPushButton):
        # todo: here we have to send the coordinates to the server -> the server is gonna check, if the send
        #  coordinates are in the other client's coordinates-array:
        # todo: server returns bool "True" if clicked button-coordinates matches the other clients-coordinate - else
        #  return bool "False"

        # todo: check is either bool "False" or "True", depending on the server answer

        check: bool

        # if-statement for testing
        if ((coordinates[0] + coordinates[1]) % 2) == 0:
            check = True
        else:
            check = False

        # actual code
        if check:
            button.setStyleSheet("background-color: red")

        if not check:
            button.setStyleSheet("background-color: gray")


class StatsLayout(QVBoxLayout):
    def __init__(self, parent: MainWindow):
        super().__init__()
        self.parent: MainWindow = parent
        self.layout = QVBoxLayout()

    def run(self):
        label = QLabel("Player-Stats")
        self.layout.addWidget(label)

        self.parent.layout.addLayout(self.layout)


# todo: maybe we don't need this one => gonna use pictures instead
class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
