import sys

from PyQt6.QtWidgets import QApplication

from database import *
from gui.place_ship_ui import MainWindow

# from network.common import encode_packet, decode_packet
# from src.network.client import Client

# hardcoded for testing
ship_uuid = 0
ship_form = [[0, 0], [0, 1], [0, 2]]
ship_coordinates = [5, 5, 0]


def gui_window_handler() -> None:
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    main_window.run()

    try:
        app.exec()
    except KeyboardInterrupt:
        raise KeyboardInterrupt


def main():
    # gui_window_handler()
    # print(Client().connect())
    """db = DatabaseHelper()
    db.update_schema()
    db.connect()"""
    # from src.cli.fleet_creator import board
    # [print(ele) for ele in board]
    # Ship(ship_uuid, ship_form, ship_coordinates).run()
    gui_window_handler()

    # print(Client().connect())


if __name__ == '__main__':
    main()
