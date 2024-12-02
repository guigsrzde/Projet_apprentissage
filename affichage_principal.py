from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Menu(QWidget):
    def __init__(self):
        super().__init__()  # Correct usage of super().__init__()
        self._build_ui()
        self.resize(500, 256)

    def _add_button(self, text, row, col, cb):
        button = QPushButton(text)
        button.setSizePolicy(button.sizePolicy().Expanding, button.sizePolicy().Expanding) # Make buttons resizable
        self._grid.addWidget(button, row, col)  # Add the button to the grid
        button.clicked.connect(cb)

    def _build_ui(self):
        self.setWindowTitle("Serious Game: Réussiras-tu à faire disparaître l'humanité")
        self._grid = QGridLayout()  # Create a QGridLayout
        self.setLayout(self._grid)  # Set the QGridLayout as the main layout of the window
        self.image_label = QLabel(self)

        # Load an image using QPixmap
        self.pixmap = QPixmap("map.png")  # Replace with your image path

        # Set the image to the QLabel
        self.image_label.setPixmap(self.pixmap)

        # Optional: Resize the image to fit the label size
        self.image_label.setScaledContents(True)  # Makes sure the image scales to fit the label

        # Add the QLabel to the grid layout (position 0, 0)
        self._grid.addWidget(self.image_label, 0, 0, 3, 1)

        # Add buttons on the right side (column 3)
        self._add_button("Propagation", 0, 1, self._click_propagation)
        self._add_button("Resistance", 1, 1, self._click_resistance)
        self._add_button("Symptome", 2, 1, self._click_symptome)
        self._grid.setColumnStretch(0, 2)  # Column 0 (image) gets 2x more space
        self._grid.setColumnStretch(1, 1)  # Column 1 (buttons) gets 1x space

    def _click_propagation(self):
        print("Click de propagation")

    def _click_resistance(self):
        print("Click de resistance")

    def _click_symptome(self):
        print("Click de symptome")

    def resizeEvent(self, event):
        """
        This method will be called whenever the window is resized.
        We can use this to scale the image appropriately.
        """
        width = event.size().width()
        height = event.size().height()

        max_width = 3 * width // 4
        max_height = height 

        min_width = 100
        min_height = 100

        # Ensure the image doesn't scale below the threshold
        new_width = max(min_width, min(max_width, self.pixmap.width()))
        new_height = max(min_height, min(max_height, self.pixmap.height()))

        # Resize the pixmap based on the new window size
        scaled_pixmap = self.pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio)

        # Set the scaled pixmap to the QLabel
        self.image_label.setPixmap(scaled_pixmap)

        # Optionally call the base class's resizeEvent to ensure the layout behaves properly
        super().resizeEvent(event)


def affiche():
    print("ok affichage")
    return 0
