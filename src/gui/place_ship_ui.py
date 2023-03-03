from functools import partial
from math import floor

from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, \
    QMessageBox

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

SHIPS: list[[int, [[int, int]]]] = \
    [
        [0, [[0, 0], [1, 0], [2, 0]]],
        [1, [[0, 0], [0, 1], [0, 2]]],
        [2, [[0, 0], [1, 0]]],
        [3, [[0, 0]]],
        [4, [[0, 0], [1, 0], [2, 0], [1, 1], [2, 1], [3, 1]]]
    ]

PLACED_SHIPS: list[[int, [[int, int], [int, int, int]]]] = []
USED_COORDINATES: list[[int, int]] = []


class ShipPlacement(QMainWindow):
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
    def __init__(self, parent: ShipPlacement):
        super().__init__()
        self.parent: ShipPlacement = parent
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

        self.parent.layout.addLayout(self.layout)


class Ship:
    def __init__(self, parent: PlayerGridLayout, ship: list[int, [[int, int]], [int, int, int]]):
        super().__init__()
        self.parent: PlayerGridLayout = parent

        self.ship: list[int, [[int, int]], [int, int, int]] = ship
        self.uuid: int = ship[0]
        self.form: list[[int, int]] = ship[1]
        self.root_coordinate: list[int, int, int] = ship[2]
        self.coordinates: list[[int]] = []

    def run(self):
        self.get_coordinates_with_rotation()
        self.place_ship()

    def get_coordinates_with_rotation(self):
        for element in self.form:
            relative_x, relative_y = (ele for ele in element)
            relative_x, relative_y = ROTATION_MAP[self.root_coordinate[2]](relative_x, relative_y)
            self.coordinates.append([self.root_coordinate[1] + relative_y, self.root_coordinate[0] + relative_x])

    def place_ship(self):
        for element in self.parent.buttons:
            for ele in self.coordinates:
                if element[0] == ele:
                    if element[0] == self.coordinates[0]:
                        element[1].setStyleSheet("background-color: blue")
                    else:
                        element[1].setStyleSheet("background-color: red")


class PlaceShipUI(QVBoxLayout):
    def __init__(self, parent: ShipPlacement):
        super().__init__()
        self.parent: ShipPlacement = parent
        self.layout = QVBoxLayout()

        # children
        self.display_ship_settings = DisplayShipSettings(self)

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
        self.ships: list[[int, [[int, int]], [int, int, int]]] = SHIPS

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

        for i in range(len(SHIP_BUTTONS)):
            button = QPushButton(SHIP_BUTTONS[i])
            self.layout.addWidget(button, 0, i)

            self.settings_buttons.append([SHIP_BUTTONS[i], button])

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
            self.parent.create_ship_preview.create_preview_field()

        elif _type == "rotate left":
            if self.parent.rotation == 3:
                self.parent.rotation = 0

            else:
                self.parent.rotation += 1

            self.parent.create_ship_preview.clear_preview_field()
            self.parent.create_ship_preview.create_preview_field()


        elif _type == "rotate right":
            if self.parent.rotation == 0:
                self.parent.rotation = 3

            else:
                self.parent.rotation -= 1

            self.parent.create_ship_preview.clear_preview_field()
            self.parent.create_ship_preview.create_preview_field()


        elif _type == "->":
            if self.parent.uuid == self.parent.ships[-1][0]:
                self.parent.uuid = self.parent.ships[0][0]
                self.parent.create_ship_preview.clear_preview_field()
                self.parent.create_ship_preview.create_preview_field()

            else:
                self.parent.uuid += 1
                self.parent.create_ship_preview.clear_preview_field()
                self.parent.create_ship_preview.create_preview_field()


class CreateShipPreview(QGridLayout):
    def __init__(self, parent: DisplayShipSettings):
        super().__init__()
        self.parent: DisplayShipSettings = parent
        self.layout = QGridLayout()

        self.ship_preview_buttons: list[[[int, int], object]] = []
        self.ship_field_buttons: list[[[int, int], object]] = \
            self.parent.parent.parent.game_layout.player_buttons_grid_layout.buttons

    def run(self):
        self.layout.setSpacing(0)
        self.create_preview_field()
        self.ship_field_on_click_handler()

        self.parent.layout.addLayout(self.layout)

    def create_preview_field(self):
        current_ship: list[[int, int]] = []

        for ele in self.parent.ships:
            for e in ele:
                if e == self.parent.uuid:
                    current_ship = ele[1]

        min_field_width = max(current_ship)[0] - min(current_ship)[0] + 1
        min_field_height = max(current_ship)[1] - min(current_ship)[1] + 1

        field_size = max(min_field_width, min_field_height) + 2
        field_size = max(field_size, 5)
        field_size += (field_size % 2 == 0)
        field_center = floor(field_size / 2)

        current_ship = [ROTATION_MAP[self.parent.rotation](tile[0], tile[1]) for tile in current_ship]

        self.layout.addWidget(QLabel(), 0, 0)
        for y in range(field_size):
            self.layout.addWidget(QLabel(), y + 1, 0)  # space left
            for x in range(field_size):
                button = QPushButton()
                button.setFixedSize(32, 32)

                self.ship_preview_buttons.append([[x, y], button])
                self.layout.addWidget(button, y + 1, x + 1)

                button.setStyleSheet(f"background-color: red") if [x - field_center, y - field_center] in current_ship \
                    else button.setStyleSheet(f"background-color: transparent")
                button.setStyleSheet(f"background-color: blue") if [x - field_center, y - field_center] == current_ship[
                    0] else None

            self.layout.addWidget(QLabel(), y + 1, field_size + 1)  # space right
        self.layout.addWidget(QLabel(), field_size + 1, 0)  # space bottom

    def clear_preview_field(self):
        [self.layout.itemAt(ele).widget().deleteLater() for ele in range(self.layout.count())]

    def ship_field_on_click_handler(self):
        [ele[1].clicked.connect(partial(self.connect_preview_with_ship_field, ele[0])) for ele in
         self.ship_field_buttons]

    def check_for_overlapping(self, ship) -> bool:
        coordinates = []

        for element in ship[1]:
            relative_x, relative_y = (ele for ele in element)
            relative_x, relative_y = ROTATION_MAP[ship[2][2]](relative_x, relative_y)
            coordinates.append([ship[2][1] + relative_y, ship[2][0] + relative_x])

        for element in USED_COORDINATES:
            for ele in coordinates:
                if ele in element:
                    return False

        for element in coordinates:
            for ele in element:
                if ele > 12:
                    return False

        USED_COORDINATES.append(coordinates)
        return True

    def connect_preview_with_ship_field(self, cords: list[int, int]):
        for ele in self.parent.ships:
            if self.parent.uuid in ele:
                current_ship: list[int, [[int, int]], [int, int, int]] = [ele[0], ele[1], [cords[1], cords[0],
                                                                                           self.parent.rotation]]

                check = self.check_for_overlapping(current_ship)

                if check:
                    PLACED_SHIPS.append(current_ship)
                    ship = Ship(self.parent.parent.parent.game_layout.player_buttons_grid_layout, current_ship)
                    ship.run()

                    self.parent.ships.remove(ele)
                    self.clear_preview_field()

                    if len(self.parent.ships) != 0:
                        self.parent.uuid = min(self.parent.ships)[0]
                        self.create_preview_field()

                    else:
                        [ele[1].deleteLater() for ele in self.parent.create_settings_button.settings_buttons]

                        finish_alert = QMessageBox(self.parent.parent.parent)
                        finish_alert.setWindowTitle("Alert")
                        finish_alert.setText("Successfully placed all ships correct or out of game-field")
                        finish_alert.setStandardButtons(QMessageBox.StandardButton.Close)
                        finish_alert.setIcon(QMessageBox.Icon.Information)

                        finish_alert.exec()

                        # todo: here we should send "PLACED_SHIPS" / "USED_COORDINATES" to the server (probably "USED_COORDINATES")

                        self.parent.parent.parent.close()

                else:
                    finish_alert = QMessageBox(self.parent.parent.parent)
                    finish_alert.setWindowTitle("Alert")
                    finish_alert.setText("Ship is overlapping with another one or is out of game-field")
                    finish_alert.setStandardButtons(QMessageBox.StandardButton.Close)
                    finish_alert.setIcon(QMessageBox.Icon.Critical)

                    finish_alert.exec()


# todo: maybe we don't need this one => gonna use pictures instead
class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
