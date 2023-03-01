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

# todo: because "rotate right" doesn't work right now
# SHIP_BUTTONS: list[str] = [
#     "<-",
#     "rotate left",
#     "rotate right",
#     "->",
# ]

SHIP_BUTTONS: list[str] = [
    "<-",
    "rotate",
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


ships: list[[int, [[int, int]], [int, int, int]]] = \
    [
        # uuid, layout, root-coordinate
        [0, [[0, 0], [1, 0], [2, 0]]],
        [1, [[0, 0], [0, 1], [0, 2]]],
        [2, [[0, 0], [1, 0]]],
        [3, [[0, 0]]],
        [4, [[0, 0], [1, 0], [2, 0], [1, 1], [2, 1], [3, 1]]]
    ]


class PlayerGridLayout(QGridLayout):
    def __init__(self, parent: GameLayout):
        super().__init__()
        self.parent: GameLayout = parent
        self.buttons: list[[[int, int], object]] = []
        self.layout = QGridLayout()

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
    def __init__(self, parent: PlayerGridLayout, ship: list[int, [[int, int]], [int, int, int]]):
        super().__init__()
        self.parent: PlayerGridLayout = parent

        self.ship: list[int, [[int, int]], [int, int, int]] = ship
        self.uuid: int = ship[0]
        self.form: [[int, int]] = ship[1]
        self.root_coordinate: [int, int, int] = ship[2]
        self.coordinates: list[[int, int]] = []
        print("ship[2]", ship[2])

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

            self.parent.rotation = 0
            self.parent.create_ship_preview.clear_preview_field()
            self.parent.create_ship_preview.create_ship_field()

        if _type == "rotate":
            if self.parent.rotation == 0:
                self.parent.rotation = 3

            else:
                self.parent.rotation -= 1

            self.parent.create_ship_preview.clear_preview_field()
            self.parent.create_ship_preview.create_ship_field()

        # todo: because "rotate right" doesn't work right now
        # if _type == "rotate left":
        #     if self.parent.rotation == 0:
        #         self.parent.rotation = 3
        #
        #     else:
        #         self.parent.rotation -= 1
        #
        #     self.parent.create_ship_preview.clear_preview_field()
        #     self.parent.create_ship_preview.create_ship_field()

        # [print("cords:", ele[0]) for ele in self.parent.create_ship_preview.ship_preview_buttons]

        # if _type == "rotate right":
        #     if self.parent.rotation == 3:
        #         self.parent.rotation = 0
        #
        #     else:
        #         self.parent.rotation += 1
        #
        #     self.parent.create_ship_preview.clear_preview_field()
        #     self.parent.create_ship_preview.create_ship_field()

        # [print("cords:", ele[0]) for ele in self.parent.create_ship_preview.ship_preview_buttons]

        if _type == "->":
            if self.parent.uuid == self.parent.ships[-1][0]:
                self.parent.uuid = self.parent.ships[0][0]

            else:
                self.parent.uuid += 1

            self.parent.rotation = 0
            self.parent.create_ship_preview.clear_preview_field()
            self.parent.create_ship_preview.create_ship_field()


class CreateShipPreview(QGridLayout):
    def __init__(self, parent: DisplayShipSettings):
        super().__init__()
        self.parent: DisplayShipSettings = parent
        self.layout = QGridLayout()

        self.field_buttons: list[[[int, int], object]] = \
            self.parent.parent.parent.game_layout.player_buttons_grid_layout.buttons
        self.ship_preview_buttons: list[[[int, int], object]] = []

    def run(self):
        self.create_ship_field()
        self.connect_button_with_ship()

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
                # button.setFixedSize(50, 50)
                self.ship_preview_buttons.append([[i, j], button])

                button.setStyleSheet(f"background-color: red") if [i, j] in current_ship else button.hide()
                button.setStyleSheet(f"background-color: blue") if [i, j] == current_ship[0] else None

                self.layout.addWidget(button, j, i)

        # [print("ele:", ele) for ele in self.ship_preview_buttons]

        self.parent.layout.addLayout(self.layout)

    def cycle_rotation(self, ship: list[[int, int]]):
        if self.parent.rotation == 0:
            # print(self.parent.rotation)
            ship.reverse()
            [ele.reverse() for ele in ship]
        if self.parent.rotation == 1:
            # print(self.parent.rotation)
            [ele.reverse() for ele in ship]
        if self.parent.rotation == 2:
            # print(self.parent.rotation)
            ship.reverse()
            [ele.reverse() for ele in ship]
        if self.parent.rotation == 3:
            # print(self.parent.rotation)
            [ele.reverse() for ele in ship]

        return ship

    def clear_preview_field(self):
        for ele in self.ship_preview_buttons:
            ele[1].deleteLater()

        self.ship_preview_buttons = []

    def connect_button_with_ship(self):
        [ele[1].clicked.connect(partial(self.button_clicked_handler, ele[0], ele[1])) for ele in self.field_buttons]

    def button_clicked_handler(self, cords: list[int, int], button: object):
        # Ship(self, ships[0][0], ships[0][1], ships[0][2])

        for ele in self.parent.ships:
            if self.parent.uuid in ele:
                print("rotation", self.parent.rotation)
                current_ship: list[int, [[int, int]], [int, int, int]] = [ele[0], reversed(ele[1]), [cords[1], cords[0],
                                                                                                     self.parent.rotation]]

                print("rotation", self.parent.rotation)
                ship = Ship(self.parent.parent.parent.game_layout.player_buttons_grid_layout, current_ship)
                ship.run()


# todo: maybe we don't need this one => gonna use pictures instead
class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
