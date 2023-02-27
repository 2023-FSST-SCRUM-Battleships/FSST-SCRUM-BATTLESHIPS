import sys
from PyQt6.QtWidgets import QApplication

from comps.gui import MainWindow
from network.common import encode_packet, decode_packet
from network.client import Client

from database import *

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
    #gui_window_handler()
    #print(Client().connect())
    db = DatabaseHelper()
    db.update_schema()
    db.connect()


if __name__ == '__main__':
    main()
