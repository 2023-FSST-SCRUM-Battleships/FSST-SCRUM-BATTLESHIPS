import sys

from PyQt6.QtWidgets import QApplication

from gui.login_register_gui import LoginAndRegister


def gui_window_handler() -> None:
    app = QApplication(sys.argv)

    main_window = LoginAndRegister()
    main_window.show()
    main_window.run()

    try:
        app.exec()
    except KeyboardInterrupt:
        raise KeyboardInterrupt


def main():
    gui_window_handler()

    # print(Client().connect())


if __name__ == '__main__':
    main()
