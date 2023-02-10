import sys
from PyQt6.QtWidgets import QApplication

from comps.gui import MainWindow, ButtonGridLayout


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


if __name__ == '__main__':
    main()
