#import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Hauptwidget und Rasterlayout
        self.central_widget = QWidget(self)
        self.grid_layout = QGridLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        #Schaltflächen
        for row in range(12):
            for column in range(12):
                button = QPushButton("", self.central_widget)
                button.setFixedSize(30, 30) # Größe der Schaltfläche
                button.clicked.connect(lambda checked, r=row, c=column: self.place_ship(r, c))
                self.grid_layout.addWidget(button, row, column)

        #Rasterlayout als Layout des Hauptwidgets
        self.central_widget.setLayout(self.grid_layout)

        #eine Liste für den Zustand jedes Feldes
        self.field = [[0] * 12 for _ in range(12)]

    def place_ship(self, row, column):
        #check ob schiff auf dieser Zelle bereits platziert wurde
        if self.field[row][column] == 1:
            QMessageBox.warning(self, "Achtung", "Sie haben bereits ein Schiff auf diesem Feld platziert!")
            return

        # Schiff auf Zelle und markieren entsprechenden Zellen
        self.field[row][column] = 1
        self.grid_layout.itemAtPosition(row, column).widget().setStyleSheet("background-color: blue;")

        # Überprüfen ob alle Schiffe platziert wurden
        if self.all_ships_placed():
            QMessageBox.information(self, "Fertig", "Alle Schiffe wurden platziert!")

    def all_ships_placed(self):
        for row in range(12):
            for column in range(12):
                if self.field[row][column] == 0:
                    return False
        return True

#für test
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
"""