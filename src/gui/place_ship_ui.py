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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()

        # children
        self.game_layout = GameLayout(self)
        self.place_ship_ui = PlaceShipUI(self)

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
        self.place_ship_ui.run()


class GameLayout(QVBoxLayout):
    def __init__(self, parent: MainWindow):
        super().__init__()
        self.parent: MainWindow = parent
        self.layout = QVBoxLayout()

        # children
        self.player_buttons_grid_layout = PlayerGridLayout(self)

    def run(self):
        label = QLabel("Game Field")
        self.layout.addWidget(label)

        label = QLabel("Player")
        self.layout.addWidget(label)
        self.player_buttons_grid_layout.run()

        self.parent.layout.addLayout(self.layout)


# hardcoded for testing "Ship"
ship_uuid: int = 0
ship_form: list[[int, int]] = [[0, 0], [1, 0], [2, 0], [1, 1], [2, 1], [3, 1]]
ship_coordinates: list[int, int, int] = [5, 5, 1]

ships: list[[int, [[int, int]], [int, int, int]]] = \
    [
        # uuid, layout, root-coordinate
        [0, [[0, 0], [1, 0], [2, 0]], [8, 2, 0]],
        [1, [[0, 0], [0, 1], [0, 2]], [0, 2, 0]],
        [2, [[0, 0], [1, 0]], [9, 10, 2]],
        [3, [[0, 0]], [3, 3, 3]],
        [4, [[0, 0], [1, 0], [2, 0], [1, 1], [2, 1], [3, 1]], [6, 6, 3]]
    ]


class PlayerGridLayout(QGridLayout):
    def __init__(self, parent: GameLayout):
        super().__init__()
        self.parent: GameLayout = parent
        self.buttons: list[[[int, int], object]] = []
        self.layout = QGridLayout()

        # children
        self.ship_1 = Ship(self, ships[0][0], ships[0][1], ships[0][2])
        self.ship_2 = Ship(self, ships[1][0], ships[1][1], ships[1][2])
        self.ship_3 = Ship(self, ships[2][0], ships[2][1], ships[2][2])
        self.ship_4 = Ship(self, ships[3][0], ships[3][1], ships[3][2])
        self.ship_5 = Ship(self, ships[4][0], ships[4][1], ships[4][2])

    def run(self):
        self.render_button_layout()
        self.ship_1.run()
        self.ship_2.run()
        self.ship_3.run()
        self.ship_4.run()
        self.ship_5.run()

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
    def __init__(self, parent: PlayerGridLayout, uuid: int, form: list[[int, int]], coordinates: list[int, int, int]):
        super().__init__()
        self.parent: PlayerGridLayout = parent

        # self.ships: list[[int, [[int, int]], [int, int, int]]] = ships
        self.uuid: int = uuid
        self.form: list[[int, int]] = form
        self.root_coordinate: list[int, int, int] = coordinates
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

        # print(f"coordinates: {self.coordinates[0]}")

    def place_ship(self):
        for element in self.parent.buttons:
            for ele in self.coordinates:
                if element[0] == ele:
                    if element[0] == self.coordinates[0]:
                        element[1].setStyleSheet("background-color: blue")
                    else:
                        element[1].setStyleSheet("background-color: red")


class PlaceShipUI(QVBoxLayout):
    def __init__(self, parent: MainWindow):
        super().__init__()
        self.parent: MainWindow = parent
        self.layout = QVBoxLayout()

        # children
        self.display_ship_settings = DisplayShipSettings(self)
        # DisplayShipSettings hardcoded for testing

    def run(self):
        self.display_ship_settings.run()
        self.parent.layout.addLayout(self.layout)


class DisplayShipSettings(QVBoxLayout):
    def __init__(self, parent: PlaceShipUI):
        super().__init__()
        self.parent: PlaceShipUI = parent
        self.layout = QVBoxLayout()

        self.uuid: int = 0
        self.rotation: int = 0
        self.ships: list[[int, [[int, int]], [int, int, int]]] = ships
        # [print("ships:", ele) for ele in self.ships]

        # children
        self.create_ship_preview = CreateShipPreview(self)
        self.create_settings_button = CreateSettingsButtons(self)

    def run(self):
        self.create_ship_preview.run()
        self.create_settings_button.run()

        self.parent.layout.addLayout(self.layout)


class CreateSettingsButtons(QGridLayout):
    def __init__(self, parent: DisplayShipSettings):
        super().__init__()
        self.parent: DisplayShipSettings = parent
        self.layout = QGridLayout()

        self.settings_buttons: list[[str, object]] = []

    def run(self):
        self.create_button()
        self.connect_buttons()

    def create_button(self):
        self.layout.setSpacing(1)

        # [self.layout.addWidget(QPushButton(ele)) for ele in SHIP_BUTTONS]
        for i in range(len(SHIP_BUTTONS)):
            button = QPushButton(SHIP_BUTTONS[i])
            self.layout.addWidget(button, 0, i)

            self.settings_buttons.append([SHIP_BUTTONS[i], button])

        # [print("buttons:", ele) for ele in self.settings_buttons]
        self.parent.layout.addLayout(self.layout)

    def connect_buttons(self):
        for ele in self.settings_buttons:
            ele[1].clicked.connect(partial(self.handle_clicked_button, ele[0]))

    def handle_clicked_button(self, _type):
        if _type == "<-":
            if self.parent.uuid == self.parent.ships[0][0]:
                self.parent.uuid = self.parent.ships[-1][0]

            else:
                self.parent.uuid -= 1

            self.parent.create_ship_preview.clear_preview_field()
            self.parent.create_ship_preview.create_ship_field()

        if _type == "rotate left":
            # [print("rotate left: ", ele[0]) for ele in self.parent.create_ship_preview.ship_preview_buttons]
            if self.parent.rotation == 0:
                self.parent.rotation = 3

            else:
                self.parent.rotation -= 1

            self.parent.create_ship_preview.clear_preview_field()
            self.parent.create_ship_preview.create_ship_field()

            # [print("cords:", ele[0]) for ele in self.parent.create_ship_preview.ship_preview_buttons]

        if _type == "rotate right":
            if self.parent.rotation == 3:
                self.parent.rotation = 0

            else:
                self.parent.rotation += 1

            self.parent.create_ship_preview.clear_preview_field()
            self.parent.create_ship_preview.create_ship_field()

            # [print("cords:", ele[0]) for ele in self.parent.create_ship_preview.ship_preview_buttons]

        if _type == "->":
            if self.parent.uuid == self.parent.ships[-1][0]:
                self.parent.uuid = self.parent.ships[0][0]
                self.parent.create_ship_preview.clear_preview_field()
                self.parent.create_ship_preview.create_ship_field()

            else:
                self.parent.uuid += 1
                self.parent.create_ship_preview.clear_preview_field()
                self.parent.create_ship_preview.create_ship_field()


class CreateShipPreview(QGridLayout):
    def __init__(self, parent: DisplayShipSettings):
        super().__init__()
        self.parent: DisplayShipSettings = parent
        self.layout = QGridLayout()

        self.ship_preview_buttons: list[[[int, int], object]] = []

    def run(self):
        self.create_ship_field()

    def create_ship_field(self):
        current_ship: list[[int, int]] = []

        for ele in self.parent.ships:
            for e in ele:
                if e == self.parent.uuid:
                    current_ship = ele[1]

        current_ship = self.cycle_rotation(current_ship)

        # print("current_ship, rotation:", current_ship, self.parent.rotation)

        for i in range(min(current_ship)[0], max(current_ship)[0] + 1):
            for j in range(min(current_ship)[1], (max(current_ship)[1] + 1)):
                button = QPushButton()
                self.ship_preview_buttons.append([[i, j], button])

                print([i, j], current_ship[0])
                # button.setFixedSize(50, 50)
                button.setStyleSheet(f"background-color: red") if [i, j] in current_ship else button.hide()
                button.setStyleSheet(f"background-color: blue") if [i, j] == current_ship[0] else None

                self.layout.addWidget(button, j, i)

        self.parent.layout.addLayout(self.layout)

    def cycle_rotation(self, ship: list[[int, int]]):
        if self.parent.rotation == 0:
            ship.reverse()
            [ele.reverse() for ele in ship]
        if self.parent.rotation == 1:
            [ele.reverse() for ele in ship]
        if self.parent.rotation == 2:
            ship.reverse()
            [ele.reverse() for ele in ship]
        if self.parent.rotation == 3:
            [ele.reverse() for ele in ship]

        # print(ship)
        return ship

    def clear_preview_field(self):
        for ele in self.ship_preview_buttons:
            ele[1].deleteLater()

        self.ship_preview_buttons = []


# todo: maybe we don't need this one => gonna use pictures instead
class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
