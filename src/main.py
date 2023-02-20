import sys
from PyQt6.QtWidgets import QApplication

from comps.gui import MainWindow
from src.cli.fleet_creator import fleet_creator


# from network.common import encode_packet, decode_packet
# from src.network.client import Client


def gui_window_handler():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    main_window.run()

    try:
        app.exec()
    except KeyboardInterrupt:
        raise KeyboardInterrupt


def main():
    gui_window_handler()
    # fleet_creator()
    # print(Client().connect())


if __name__ == '__main__':
    main()
