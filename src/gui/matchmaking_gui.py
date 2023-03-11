# from functools import partial
# from math import floor
#
# from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox


class Matchmaking(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.db_data = None

        # children
        self.one_player_line = OnePlayerLine(self, "Lucas", [100, 17])
        self.one_player_line_2 = OnePlayerLine(self, "Lucas", [10, 0])
        self.one_player_line_3 = OnePlayerLine(self, "Lucas", [14, 7])

    def ui(self):
        self.setWindowTitle("Titanic who-ooo")
        # self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(50)

    def run(self):
        self.get_players_from_db()

        self.ui()
        self.run_layouts()

        main_widget = QWidget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

    def run_layouts(self):
        self.one_player_line.run()
        self.one_player_line_2.run()
        self.one_player_line_3.run()

        # for ele in self.db_data:
        #     ...

    # todo: i don't know if this is gonna stay a staticmethod or go like "self."
    @staticmethod
    def get_players_from_db():
        # self.db_data
        pass


class OnePlayerLine(QMainWindow):
    def __init__(self, parent: Matchmaking, name: str, win_lose: list[int, int]):
        super().__init__()
        self.parent: Matchmaking = parent
        self.layout = QHBoxLayout()

        self.name: str = name
        self.win_lose: list[int, int] = win_lose
        self.check_box_status: bool = True

        self.parent.layout.addLayout(self.layout)

    def run(self):
        self.player_name()
        self.player_win_lose()
        self.player_checkbox()

    def player_name(self):
        label = QLabel(self.name)
        # label.setStyleSheet("border: 3px dashed blue")
        self.layout.addWidget(label)

    def player_win_lose(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)

        label_wins = QLabel(f"Wins: {self.win_lose[0]}")
        label_loses = QLabel(f"Loses: {self.win_lose[1]}")
        label_rating = QLabel(f"W-R: {int(round(self.win_lose[0] / (self.win_lose[0] + self.win_lose[1]), 2) * 100)}%")

        layout.addWidget(label_wins)
        layout.addWidget(label_loses)
        layout.addWidget(label_rating)

        self.layout.addLayout(layout)

    def player_checkbox(self):
        check_box = QCheckBox("Play against")

        self.layout.addWidget(check_box)

        check_box.clicked.connect(lambda: self.handle_clicked_check_box())

    def handle_clicked_check_box(self):
        if self.check_box_status:
            # todo: send to server that player wants to play with clicked player
            print("yes")

        if not self.check_box_status:
            # todo: send to server that player don't to play with clicked player
            print("no")

        self.check_box_status = not self.check_box_status
