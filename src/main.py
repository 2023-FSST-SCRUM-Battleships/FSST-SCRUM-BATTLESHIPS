import sys

from PyQt6.QtWidgets import QApplication

from gui.active_game_gui import MainWindow


# from network.common import encode_packet, decode_packet
# from src.network.client import Client


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
    # fleet_creator()
    gui_window_handler()

    # print(Client().connect())
    # db = DatabaseHelper()
    # db.update_schema()
    # db.connect()
    # from src.cli.fleet_creator import board
    # [print(ele) for ele in board]
    # Ship(ship_uuid, ship_form, ship_coordinates).run()

    # print(Client().connect())


if __name__ == '__main__':
    main()
