import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap

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
        self.image_label = QLabel(self)

        # Load an image using QPixmap
        pixmap = QPixmap("map.png")  # Replace with your image path

        # Set the image to the QLabel
        self.image_label.setPixmap(pixmap)

        # Optional: Resize the image to fit the label size
        self.image_label.setScaledContents(True)  # Makes sure the image scales to fit the label

        # Add the QLabel to the grid layout (position 0, 0)
        self._grid.addWidget(self.image_label, 0, 0, 3, 1)

        # Add buttons on the right side (column 3)
        self._add_button("Propagation", 0, 1, self._click_propagation)
        self._add_button("Resistance", 1, 1, self._click_resistance)
        self._add_button("Symptome", 2, 1, self._click_symptome)

    def _click_propagation(self):
        print("Click de propagation")

    def _click_resistance(self):
        print("Click de resistance")

    def _click_symptome(self):
        print("Click de symptome")



def affiche():
    print("ok affichage")
    return 0