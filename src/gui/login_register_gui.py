from functools import partial

from PyQt6.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QPushButton

FORM_FIELDS: list[str] = [
    "Username",
    "Password",
    "Confirm password"
]

FORM_BUTTONS: list[str] = [
    "Register",
    "Login"
]


class LoginAndRegister(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

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
        Fields(self).login_ui()


class Fields(QHBoxLayout):
    def __init__(self, parent: LoginAndRegister):
        super().__init__()
        self.parent: LoginAndRegister = parent
        self.layout = QVBoxLayout()

        self.login: list[[str, QLabel, QLineEdit or None]] = []
        self.register: list[[str, QLabel, QLineEdit or None]] = []

        self.parent.layout.addLayout(self.layout)

    def generate_general_form(self, _type):
        layout = QVBoxLayout()

        for ele in FORM_FIELDS:
            label = QLabel(ele)
            label.setStyleSheet("font-size: 16px")

            line = QLineEdit()
            line.setEchoMode(QLineEdit.EchoMode.Password) if ele == "Password" or ele == "Confirm password" else None

            if _type == "Login":
                self.login.append([ele, label, line])

                layout.addWidget(label)
                layout.addWidget(line)

            if _type == "Register":
                if ele != "Confirm password":
                    self.register.append([ele, label, line])
                    layout.addWidget(label)
                    layout.addWidget(line)

                if ele == "Confirm password":
                    for i in range(2):
                        label_spacer = QLabel()
                        label_spacer.setStyleSheet("font-size: 16px")

                        self.register.append(["", label_spacer])
                        layout.addWidget(label_spacer)

        self.layout.addLayout(layout)

    def clear_field(self, _type):
        if _type == "Login":
            for element in self.register:
                [ele.deleteLater() if type(ele) != str else None for ele in element]

            self.register.clear()
            self.login_ui()

        if _type == "Register":
            for element in self.login:
                [ele.deleteLater() if type(ele) != str else None for ele in element]

            self.login.clear()
            self.register_ui()

    def login_ui(self):
        self.generate_general_form("Login")

        layout = QHBoxLayout()

        for ele in FORM_BUTTONS:
            button = QPushButton(ele)
            button.setStyleSheet("background-color: lightgreen; font-size: 16px")
            button.setFixedWidth(100)

            self.login.append([ele, button])

            if ele == "Register":
                button.setStyleSheet("background-color: lightblue; font-size: 16px")
                button.clicked.connect(partial(self.clear_field, "Register"))

            layout.addWidget(button)
        self.layout.addLayout(layout)

    def register_ui(self):
        self.generate_general_form("Register")

        layout = QHBoxLayout()

        for ele in reversed(FORM_BUTTONS):
            button = QPushButton(ele)
            button.setStyleSheet("background-color: lightgreen; font-size: 16px")
            button.setFixedWidth(100)

            self.register.append([ele, button])

            if ele == "Login":
                button.setStyleSheet("background-color: lightblue; font-size: 16px")
                button.clicked.connect(partial(self.clear_field, "Login"))

            layout.addWidget(button)
        self.layout.addLayout(layout)
