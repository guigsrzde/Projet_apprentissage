import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout

class Menu(QWidget):
    def __init__(self):
        super().__init__()  # Correct usage of super().__init__()
        self._build_ui()
        self.resize(256, 256)

    def _add_button(self, text, row, col, cb):
        button = QPushButton(text)
        self._grid.addWidget(button, row, col)  # Add the button to the grid
        button.clicked.connect(cb)

    def _build_ui(self):
        self.setWindowTitle("Serious Game: Réussiras-tu à faire disparaître l'humanité")
        self._grid = QGridLayout()  # Create a QGridLayout
        self.setLayout(self._grid)  # Set the QGridLayout as the main layout of the window

        # Add buttons on the right side (column 3)
        self._add_button("Propagation", 0, 3, self._click_propagation)
        self._add_button("Resistance", 1, 3, self._click_resistance)
        self._add_button("Symptome", 2, 3, self._click_symptome)

    def _click_propagation(self):
        print("Click de propagation")

    def _click_resistance(self):
        print("Click de resistance")

    def _click_symptome(self):
        print("Click de symptome")



def affiche():
    print("ok affichage")
    return 0